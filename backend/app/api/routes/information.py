# MARK: Import
# Dependencies
from flask import jsonify

# Routes
from app.api.routes import api_bp

# Modules
from app.models.response import EvResponseModel
from app.models.intro_section import EvIntroSectionModel
from app.models.intro_title_content import EvIntroTitleContentModel
from app.models.intro_test_structure_content import EvIntroTestStructureContentModel
from app.models.icon_text import EvIconTextModel
from app.models.intro_bottom_content import EvIntroBottomContentModel
from app.models.intro_test_evaluation_content import EvIntroTestEvaluationContentModel
from app.models.intro_test_audio_content import EvIntroTestAudioContentModel

# MARK: Information
@api_bp.route('/information/test', methods = ['GET'])
def information():
    '''
    Information route for the test.
    '''
    return jsonify(EvResponseModel(
        code = 200,
        status = 'Success',
        message = 'Information retrieved successfully',
        data = [
            EvIntroSectionModel(
                title = 'Let’s get to know the test!',
                subtitle = 'What’s the IELTS Speaking test like? Let’s break it down so you don’t feel lost when it starts!',
                content = [
                    EvIntroTitleContentModel(
                        title = 'Test structure',
                        content = None,
                        sub_title = 'The test will be conducted in three parts',
                    ),
                    EvIntroTestStructureContentModel(
                        label = 'Part 1',
                        title = 'Introduction and interviews',
                        content = 'You’ll get asked simple questions about work, hobbies, or where you live. Just answer like you’re chatting with a friend.',
                        sub_title = EvIconTextModel(
                            icon_url = 'icon1.png',
                            text = 'Duration: 4-5 minutes'
                        ),
                    ),
                    EvIntroTestStructureContentModel(
                        label = 'Part 2',
                        title = 'Individual Long Turn',
                        content = 'You’ll get a topic + 1 min to think → then talk for 2 mins nonstop. Feels like a mini monologue — chill and go with the flow!',
                        sub_title = EvIconTextModel(
                            icon_url = 'icon2.png',
                            text = 'Duration: 3-4 minutes'
                        ),
                    ),
                    EvIntroTestStructureContentModel(
                        label = 'Part 3',
                        title = 'Two-way discussion',
                        content = 'Follow-up questions from Part 2. You’ll share your opinions, reasons, and go a bit deeper in thought.',
                        sub_title = EvIconTextModel(
                            icon_url = 'icon3.png',
                            text = 'Duration: 3-4 minutes'
                        ),
                    ),
                    EvIntroBottomContentModel(
                        bottom_text = 'Scoring criteria',
                        information = 'Tap here to see what the AI examiner is actually looking for.',
                    )
                ],
            ),
            EvIntroSectionModel(
                title = 'What Are You Really Judged On?',
                subtitle = 'There are 4 key things we’re paying attention to. Not to judge — but to help you grow. 😉',
                content = [
                    EvIntroTestEvaluationContentModel(
                        title = 'Fluency & Coherence',
                        subtitle = 'Can you speak smoothly and connect your thoughts clearly?',
                        content = [
                            'No need to rush — just talk like you\'re telling a story that flows.',
                            'Just make it flows, avoid "umm, ahh.."',
                        ],
                        icon_url = 'https://example.com/icon.png'
                    ),
                    EvIntroTestEvaluationContentModel(
                        title = 'Lexical Resource',
                        subtitle = 'Are you using a good mix of words?',
                        content = [
                            'Try new vocab, don’t repeat the same words. Sprinkle in expressions that show your personality!',
                            'Avoid using same vocabularies..',
                        ],
                        icon_url = 'https://example.com/icon.png'
                    ),
                    EvIntroTestEvaluationContentModel(
                        title = 'Grammatical Range & Accuracy',
                        subtitle = 'Are your sentences accurate and varied?',
                        content = [
                            'Mix your sentence types — it’s okay to slip up, just show that you’ve got range.',
                            'Show various tenses and structures',
                        ],
                        icon_url = 'https://example.com/icon.png'
                    ),
                    EvIntroTestEvaluationContentModel(
                        title = 'Pronunciation',
                        subtitle = 'Is it easy to understand what you’re saying?',
                        content = [
                            'Clarity matters more than accent. Speak clearly and use natural rhythm.',
                            'Focus on clarity, not accent!',
                        ],
                        icon_url = 'https://example.com/icon.png'
                    ),
                    EvIntroBottomContentModel(
                        bottom_text = 'Let’s start the test!',
                        information = 'No one’s here to grade you harshly. Think of this as your smart practice buddy who knows what IELTS expects.',
                    )
                ],
            ),
            EvIntroSectionModel(
                title = 'Let’s Start Your IELTS Test!',
                subtitle = 'Relax — think of it like a casual conversation.',
                content = [
                    EvIntroTestAudioContentModel(
                        title = 'Check Your Audio First:',
                        mic_button = EvIconTextModel(
                            icon_url = 'icon1.png',
                            text = 'Check Mic'
                        ),
                        speaker_button = EvIconTextModel(
                            icon_url = 'icon1.png',
                            text = 'Check Speaker'
                        ),
                        tips = EvIconTextModel(
                            icon_url = 'icon1.png',
                            text = 'Tip: Use a headset for better clarity!'
                        ),
                    ),
                    EvIntroTitleContentModel(
                        title = 'Before You Start, Make Sure:',
                        sub_title = None,
                        content = [
                            'You’ve got a pen & paper ready.',
                            'Your internet is stable.',
                            'You stay on this page during the test.',
                        ],
                    ),
                    EvIntroBottomContentModel(
                        bottom_text = 'Let’s Go!! 🚀',
                        information = None,
                    ),
                ],
            ),
        ]
    ).to_dict()), 200, {'ContentType' : 'application/json'}