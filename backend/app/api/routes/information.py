# MARK: Import
# Dependencies
from flask import jsonify

# Routes
from app.api.routes import api_bp

# Modules
from app.models.response_model import EvResponseModel
from app.models.intro_section_model import EvIntroSectionModel
from app.models.intro_section_content_model import EvIntroSectionContentModel
from app.models.intro_section_content_list_model import EvIntroSectionContentListModel
from app.models.intro_speaking_introduction_model import EvIntroSpeakingIntroductionModel
from app.models.intro_speaking_introduction_list_model import EvIntroSpeakingIntroductionListModel

# MARK: Information
@api_bp.route('/information/<type>', methods = ['GET'])
def information(type):
    '''
    Information route for the test.
    '''
    if type == 'test':
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
    
    elif type == 'speaking-intro':
        return jsonify(EvResponseModel(
            code = 200,
            status = 'Success',
            message = 'Information retrieved successfully',
            data = [
                EvIntroSpeakingIntroductionModel(
                    title = 'Introduction and interviews',
                    label = 'Part 1',
                    descriptions = [
                        '<p>In this part of the test, the examiner will ask you questions about yourself and your home.</p>',
                        '<p><strong>No pressure</strong> — just imagine you\'re having a casual chat!</p>',
                    ],
                    instructions = [
                        EvIntroSpeakingIntroductionListModel(
                            title = 'You\'ll get 3-7 questions from our AI',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Speak for 30-60 seconds per question.',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Think of this as a real conversation, not a test 😊',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                    ],
                    outroMessage = 'You\'ve finished the first part of your speaking test. Keep going!',
                    nextPart= 'part 2',
                    tips= EvIntroSpeakingIntroductionListModel(
                        title = 'Practice your pronunciation daily — it can boost your band score by up to 0.5 points!',
                        image_url= 'assets/new/svg/lamp.svg',
                    ),
                ).to_dict(),
                EvIntroSpeakingIntroductionModel(
                    title = 'Individual long turn',
                    label = 'Part 2',
                    descriptions = [
                        '<p>You\'ll get 1 topic, have 1 minute to think, then speak for 1-2 minutes nonstop.</p>',
                        '<p>Just pretend you\'re telling a story to a friend.</p>',
                    ],
                    instructions = [
                        EvIntroSpeakingIntroductionListModel(
                            title = 'The topic will appear on screen (just like an IELTS task card)',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = '1 minute to prepare',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Speak solo for 1-2 minutes',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Stay relaxed, like you\'re chatting with a friend',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                    ],
                    outroMessage = 'You\'ve finished the second part of your speaking test. Keep going!',
                    nextPart= 'part 3',
                    tips= EvIntroSpeakingIntroductionListModel(
                        title = 'Use this structure: Opening - Details - Closing. It doesn\'t need to be perfect — just keep the story flowing!',
                        image_url= 'assets/new/svg/lamp.svg',
                    ),
                ).to_dict(),
                EvIntroSpeakingIntroductionModel(
                    title = 'Two-way discussion',
                    label = 'Part 3',
                    descriptions = [
                        '<p>The final part of your test.</p>',
                        '<p>You\'ll answer follow-up questions based on Part 2.</p>',
                    ],
                    instructions = [
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Listen to the question carefully.',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Wait 5 seconds after the question finishes.',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Answer with details (1-2 minutes).',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                        EvIntroSpeakingIntroductionListModel(
                            title = 'Give examples to support your answer.',
                            image_url= 'assets/new/svg/check.svg',
                        ),
                    ],
                    outroMessage = 'You\'ve finished the third part of your speaking test. Well done!',
                ).to_dict(),
            ]
        ).to_dict()), 200, {'ContentType' : 'application/json'}
    
    else:
        # MARK: InvalidType
        # Return the error message
        return jsonify(EvResponseModel(
            code = 400,
            status = 'Error',
            message = 'Invalid information type',
            data = {
                'error': {
                    'message': 'Invalid information type',
                },
            },
        ).to_dict()), 400, {'ContentType' : 'application/json'}