# MARK: Import
# Dependencies
from flask import jsonify

# Routes
from app.api.routes import api_bp

# Modules
from app.models.response import EvResponseModel
from app.models.intro_section import EvIntroSectionModel
from app.models.intro_section_content import EvIntroSectionContentModel
from app.models.intro_section_content_list import EvIntroSectionContentListModel

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
                title = 'Let\'s get to know the test!',
                subtitle = 'What\'s the IELTS Speaking test like? Let\'s break it down so you don\'t feel lost when it starts!',
                content = [
                    EvIntroSectionContentModel(
                        type = 0,
                        title = 'Test structure',
                        description = 'The test will be conducted in three parts',
                    ),
                    EvIntroSectionContentModel(
                        type = 1,
                        title = 'Introduction and interviews',
                        label = 'Part 1',
                        subtitle = 'Duration: 4-5 minutes',
                        description = 'You\'ll get asked simple questions about work, hobbies, or where you live. Just answer like you\'re chatting with a friend.',
                        image_url= 'assets/new/svg/timer.svg',
                    ),
                    EvIntroSectionContentModel(
                        type = 1,
                        title = 'Individual Long Turn',
                        label = 'Part 2',
                        subtitle = 'Duration: 3-4 minutes',
                        description = 'You\'ll get a topic + 1 min to think → then talk for 2 mins nonstop. Feels like a mini monologue — chill and go with the flow!',
                        image_url= 'assets/new/svg/timer.svg',
                    ),
                    EvIntroSectionContentModel(
                        type = 1,
                        title = 'Two-way discussion',
                        label = 'Part 3',
                        subtitle = 'Duration: 3-4 minutes',
                        description = 'Follow-up questions from Part 2. You\'ll share your opinions, reasons, and go a bit deeper in thought.',
                        image_url= 'assets/new/svg/timer.svg',
                    ),
                ],
                buttonText = 'Scoring criteria',
                information = 'Tap here to see what the AI examiner is actually looking for.'
            ).to_dict(),
            EvIntroSectionModel(
                title = 'What Are You Really Judged On?',
                subtitle = 'There are 4 key things we\'re paying attention to. Not to judge — but to help you grow. 😉',
                content = [
                    EvIntroSectionContentModel(
                        type = 2,
                        title = 'Fluency & Coherence',
                        description= 'Can you speak smoothly and connect your thoughts clearly?',
                        image_url= 'assets/new/images/fluency.webp',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'No need to rush — just talk like you\'re telling a story that flows.',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Just make it flows, avoid "umm, ahh.."',
                            ),
                        ],
                    ),
                    EvIntroSectionContentModel(
                        type = 2,
                        title = 'Lexical Resource',
                        description= 'Are you using a good mix of words?',
                        image_url= 'assets/new/images/lexical.webp',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'Try new vocab, don\'t repeat the same words. Sprinkle in expressions that show your personality!',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Avoid using same vocabularies.',
                            ),
                        ],
                    ),
                    EvIntroSectionContentModel(
                        type = 2,
                        title = 'Grammatical Range & Accuracy',
                        description= 'Are your sentences accurate and varied?',
                        image_url= 'assets/new/images/grammar.webp',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'Mix your sentence types — it\'s okay to slip up, just show that you\'ve got range.',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Show various tenses and structures.',
                            ),
                        ],
                    ),
                    EvIntroSectionContentModel(
                        type = 2,
                        title = 'Pronunciation',
                        description= 'Is it easy to understand what you\'re saying?',
                        image_url= 'assets/new/images/pronunciation.webp',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'Clarity matters more than accent. Speak clearly and use natural rhythm.',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Focus on clarity, not accent!',
                            ),
                        ],
                    ),
                ],
                buttonText = 'Let\'s start the test!',
                information = 'No one\'s here to grade you harshly. Think of this as your smart practice buddy who knows what IELTS expects.'
            ).to_dict(),
            EvIntroSectionModel(
                title = 'Let\'s Start Your IELTS Test!',
                subtitle = 'Relax — think of it like a casual conversation.',
                content = [
                    EvIntroSectionContentModel(
                        type = 3,
                        title = 'Check Your Audio First:',
                        subtitle = 'Tip: Use a headset for better clarity!',
                        image_url= 'assets/new/svg/headphone.svg',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'Check Mic',
                                image_url= 'assets/new/svg/mic.svg',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Check Speaker',
                                image_url= 'assets/new/svg/voice.svg',
                            ),
                        ],
                    ),
                    EvIntroSectionContentModel(
                        type = 0,
                        title = 'Before You Start, Make Sure:',
                        content= [
                            EvIntroSectionContentListModel(
                                title = 'You\'ve got a pen & paper ready.',
                                image_url= 'assets/new/svg/check.svg',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'Your internet is stable.',
                                image_url= 'assets/new/svg/check.svg',
                            ),
                            EvIntroSectionContentListModel(
                                title = 'You stay on this page during the test.',
                                image_url= 'assets/new/svg/check.svg',
                            ),
                        ],
                    ),
                ],
                buttonText = 'Let\'s Go!! 🚀',
            ).to_dict(),

        ]
    ).to_dict()), 200, {'ContentType' : 'application/json'}