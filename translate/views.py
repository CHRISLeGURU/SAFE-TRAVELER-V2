from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import TranslationHistory, VoiceChatSession, VoiceChatMessage
from .services.gemini_service import get_translation_with_context, chat_with_ai
from .services.tts_service import generate_speech
from .services.speech_service import transcribe_audio

@login_required
def translate_view(request):
    recent_translations = TranslationHistory.objects.filter(user=request.user)[:10]
    
    context = {
        'recent_translations': recent_translations,
    }
    return render(request, 'translate/translate.html', context)

@csrf_exempt
@login_required
def translate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', request.user.mother_tongue)
        context = data.get('context', 'general')
        
        try:
            # Get translation and context from Gemini
            result = get_translation_with_context(text, source_lang, target_lang, context)
            
            # Save to history
            TranslationHistory.objects.create(
                user=request.user,
                source_language=source_lang,
                target_language=target_lang,
                original_text=text,
                translated_text=result.get('translation', ''),
                context=context
            )
            
            # Generate audio if TTS is enabled
            audio_url = None
            if hasattr(request.user, 'usersettings') and request.user.usersettings.tts_enabled:
                audio_url = generate_speech(result.get('translation', ''), target_lang)
            
            return JsonResponse({
                'status': 'success',
                'translation': result.get('translation'),
                'cultural_context': result.get('cultural_context'),
                'response_suggestion': result.get('response_suggestion'),
                'pronunciation_tip': result.get('pronunciation_tip'),
                'audio_url': audio_url
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def start_voice_chat(request):
    if request.method == 'POST':
        # Create new chat session
        session_id = str(uuid.uuid4())
        session = VoiceChatSession.objects.create(
            user=request.user,
            session_id=session_id
        )
        
        return JsonResponse({
            'status': 'success',
            'session_id': session_id
        })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def process_voice_input(request):
    if request.method == 'POST':
        # Handle audio file upload and processing
        audio_file = request.FILES.get('audio')
        session_id = request.POST.get('session_id')
        
        if not audio_file or not session_id:
            return JsonResponse({'status': 'error', 'message': 'Missing audio or session'})
        
        try:
            session = VoiceChatSession.objects.get(session_id=session_id, user=request.user)
            
            # Transcribe audio
            transcription = transcribe_audio(audio_file)
            
            # Save user message
            user_message = VoiceChatMessage.objects.create(
                session=session,
                message_type='user',
                text_content=transcription.get('text', ''),
                language_detected=transcription.get('language', 'unknown'),
                audio_file=audio_file
            )
            
            # Get AI response
            ai_response = chat_with_ai(
                transcription.get('text', ''), 
                context=f"Travel assistant for {request.user.mother_tongue} speaker"
            )
            
            # Save AI message
            ai_message = VoiceChatMessage.objects.create(
                session=session,
                message_type='ai',
                text_content=ai_response
            )
            
            # Generate speech for AI response
            audio_url = None
            if hasattr(request.user, 'usersettings') and request.user.usersettings.tts_enabled:
                audio_url = generate_speech(ai_response, request.user.mother_tongue)
            
            return JsonResponse({
                'status': 'success',
                'user_text': transcription.get('text'),
                'ai_response': ai_response,
                'audio_url': audio_url,
                'language_detected': transcription.get('language')
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def text_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        
        if not session_id:
            # Create new session for text chat
            session_id = str(uuid.uuid4())
            session = VoiceChatSession.objects.create(
                user=request.user,
                session_id=session_id
            )
        else:
            session = VoiceChatSession.objects.get(session_id=session_id, user=request.user)
        
        # Save user message
        user_message = VoiceChatMessage.objects.create(
            session=session,
            message_type='user',
            text_content=message
        )
        
        # Get AI response
        ai_response = chat_with_ai(
            message, 
            context=f"Travel assistant for {request.user.mother_tongue} speaker in {getattr(session, 'current_location', 'unknown location')}"
        )
        
        # Save AI message
        ai_message = VoiceChatMessage.objects.create(
            session=session,
            message_type='ai',
            text_content=ai_response
        )
        
        return JsonResponse({
            'status': 'success',
            'response': ai_response,
            'session_id': session_id
        })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def end_voice_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        try:
            session = VoiceChatSession.objects.get(session_id=session_id, user=request.user)
            session.is_active = False
            session.save()
            
            return JsonResponse({'status': 'success'})
        except VoiceChatSession.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session not found'})
    
    return JsonResponse({'status': 'error'})