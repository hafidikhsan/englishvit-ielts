# MARK: Imports
# Dependency
import random

# Modules
from app.models.overall_evaluation_model import EvOverallEvaluationModel
from app.utils.rounded_ielts_band import EvRoundedIELTSBand

# MARK: OverallFeedbackService
class OverallFeedbackService:
    '''
    OverallFeedbackService is a class that provides methods to generate overall feedback for a given IELTS score.
    It includes methods to get the overall feedback, get the overall feedback by band, and get the overall feedback by category
    based on the EvOverallEvaluationModel.
    '''
    # MARK: Properties
    def __init__(self):
        '''
        Initializes the OverallFeedbackService with an EvEvaluationModel instance.
        '''

    # MARK: EvaluateOverallFeedback
    def evaluate_overall_feedback(self, fluency: list, lexical: list, grammar: list, pronunciation: list) -> EvOverallEvaluationModel:
        '''
        Evaluates the overall feedback based on the given lists of fluency, lexical, grammar, and pronunciation feedback.
        This method generates a new EvOverallEvaluationModel instance with the overall feedback.
        '''
        # Get average bands
        fluency_band = sum([item['ielts_band'] for item in fluency]) / len(fluency)
        fluency_band = EvRoundedIELTSBand(fluency_band).rounded_band
        lexical_band = sum([item['ielts_band'] for item in lexical]) / len(lexical)
        lexical_band = EvRoundedIELTSBand(lexical_band).rounded_band
        grammar_band = sum([item['ielts_band'] for item in grammar]) / len(grammar)
        grammar_band = EvRoundedIELTSBand(grammar_band).rounded_band
        pronunciation_band = sum([item['ielts_band'] for item in pronunciation]) / len(pronunciation)
        pronunciation_band = EvRoundedIELTSBand(pronunciation_band).rounded_band
        overall_band = (fluency_band + lexical_band + grammar_band + pronunciation_band) / 4
        overall_band = EvRoundedIELTSBand(overall_band).rounded_band

        # Get overall feedback
        overall_feedback = ''

        # Mapping feedback based on the average bands
        if overall_band >= 9.0:
            # List of potential feedback
            potential_feedback = [
                'Your responses were clear, detailed, and very well-structured. You used an impressive range of vocabulary and complex grammatical structures accurately. There were no noticeable errors, and you spoke with natural fluency and confidence throughout, making your speech sound very polished.',
                'You communicated your ideas exceptionally well, using a wide range of vocabulary and grammar with almost perfect accuracy. Your responses were detailed and coherent, and you spoke fluently without hesitation. You demonstrated a high level of control over your language skills.',
                'Your speech was fluent, clear, and perfectly organized. You used a broad range of vocabulary and advanced grammatical structures accurately. There were no mistakes, and your pronunciation was clear, making your responses sound completely natural and professional.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 8.5:
            # List of potential feedback
            potential_feedback = [
                'Your responses were fluent, natural, and very well-organized. You used a broad range of vocabulary and grammatical structures with almost no errors. You demonstrated a high level of confidence and clarity in your speech, making it easy to understand and follow your ideas.',
                'You spoke confidently and fluently, using a wide range of vocabulary and complex structures with very few mistakes. Your pronunciation and grammar were nearly flawless, and you were able to express your ideas clearly and in detail, making your speech sound very polished.',
                'You communicated your ideas in a clear, detailed, and organized way. Your fluency was exceptional, and you used a range of vocabulary and grammatical structures accurately. The few minor mistakes you made had little impact on the clarity of your message, showcasing your strong language skills.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 8.0:
            # List of potential feedback
            potential_feedback = [
                'You spoke with great fluency and accuracy, and your responses were clear and detailed. There were very few minor errors, and your vocabulary was wide and used effectively. Your speaking was natural and confident, and you demonstrated strong control over your language.',
                'Your answers were well-structured and detailed, with very few mistakes. You used a wide range of vocabulary and grammatical structures, speaking fluently and confidently. Your minor errors did not hinder understanding, and your overall performance was impressive.',
                'You communicated your ideas clearly and confidently, with a great range of vocabulary and strong grammatical control. There were only very minor mistakes that didn\'t impact your fluency. You were able to speak naturally and without hesitation, making your responses sound very polished.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 7.5:
            # List of potential feedback
            potential_feedback = [
                'Your responses were well-organized and clear, with only occasional minor mistakes. You used a good range of vocabulary and demonstrated strong fluency. There were a few small errors in grammar, but overall, your speaking was very confident and natural.',
                'You communicated your ideas effectively with only a few minor errors. Your speech was fluent, and you used a wide range of vocabulary. Although there were some small mistakes, they did not affect your overall clarity or understanding.',
                'You gave clear, detailed responses with good control of grammar and vocabulary. Your fluency was strong, but there were a few minor issues with accuracy. Keep focusing on polishing your grammar for even more natural, error-free speech.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 7.0:
            # List of potential feedback
            potential_feedback = [
                'You gave clear, well-structured responses with only occasional mistakes. Your vocabulary and grammar were strong, but there were still a few minor errors. You spoke fluently and with good confidence. Keep working on polishing your accuracy and natural phrasing.',
                'Your responses were clear and easy to follow, with only small errors in grammar and word choice. You spoke with good fluency and confidence, though there were moments when your sentences could have been more complex. With more practice, you\'ll refine your speaking further.',
                'You showed good control of language, with a clear structure and only occasional grammar or vocabulary errors. Your responses were fluent, and you communicated your ideas effectively. Keep focusing on making your speech more natural and varied to achieve even higher fluency.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 6.5:
            # List of potential feedback
            potential_feedback = [
                'You communicated your ideas well, and your sentences were generally clear, but there were still some occasional grammar and vocabulary mistakes. You were mostly fluent, but there were moments where your response could have been more natural. Keep practicing to improve your overall fluency and accuracy.',
                'You were able to express yourself clearly with only minor mistakes in grammar and vocabulary. There were some parts that were slightly awkward, but you still conveyed your ideas effectively. With more practice, you\'ll be able to speak with more confidence and less hesitation.',
                'Your answers were fairly well-structured, and your meaning was clear, though there were occasional errors. You showed good control over your language, but some small mistakes affected the flow. Keep working on your grammar and vocabulary for even smoother responses.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 6.0:
            # List of potential feedback
            potential_feedback = [
                'You were able to give clear answers, but there were still some noticeable grammar and vocabulary mistakes. Your ideas came across, but the mistakes affected the fluency of your speech. Keep working on accuracy and using more varied sentence structures.',
                'You spoke clearly and were mostly understood, but there were occasional mistakes with grammar and word choice. Your responses were generally good, but they lacked the smoothness of a more fluent speaker. Keep practicing to improve your confidence and natural flow.',
                'You gave decent answers, and your ideas were generally clear, but you made some errors in grammar and vocabulary. There was a little repetition, and some sentences felt incomplete. More practice with complex sentences and better word choice will help you improve.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 5.5:
            # List of potential feedback
            potential_feedback = [
                'You gave more complete answers, but there were still some grammar mistakes and awkward sentences. You communicated your ideas, but some parts were unclear. Keep practicing to build more confidence and improve your sentence flow.',
                'Your response was generally understandable, but you made quite a few errors with grammar and vocabulary. While your meaning came across, it wasn\'t always smooth or accurate. With more practice, you\'ll be able to express yourself more clearly.',
                'You were able to express most of your ideas, but there were some mistakes that made it harder to follow. Your sentences were a little repetitive, and there were grammar issues. Keep working on expanding your vocabulary and improving your grammar.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 5.0:
            # List of potential feedback
            potential_feedback = [
                'You managed to give some answers, but they were often short and not fully clear. There were frequent grammar mistakes, and some of your ideas didn\'t come across properly. Keep practicing to improve your fluency and sentence structure.',
                'Your sentences were a bit repetitive, and it felt like you were struggling to find the right words. Although the meaning was somewhat clear, the mistakes made it harder to understand. Keep pushing yourself to use more varied vocabulary and more complete sentences.',
                'You did okay, but your response was limited by grammar and vocabulary issues. Some parts were hard to understand, and you need more practice with speaking naturally. With more practice, you\'ll become more confident and fluent.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 4.5:
            # List of potential feedback
            potential_feedback = [
                'You tried to speak, but there were a lot of pauses and grammar issues that made it hard to understand. You did manage to get your ideas out, though, even if they weren\'t fully clear. Keep practicing, and you\'ll get more comfortable.',
                'Your sentences were a bit short and disjointed, and there were frequent mistakes. Still, you did well to communicate your point. With more practice, you\'ll be able to express yourself more smoothly and accurately.',
                'You made a decent attempt, but there were many gaps in your response. Sometimes the meaning wasn\'t clear due to grammar mistakes, but you still managed to get some of your ideas across. Keep practicing to improve your fluency.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 4.0:
            # List of potential feedback
            potential_feedback = [
                'You gave a few short answers, but they didn\'t really connect into full sentences. There were a lot of pauses and grammar mistakes, which made it hard to follow. Keep practicing to build your sentence structure and fluency.',
                'Your response was basic, and it felt like you were trying to find the right words. It was hard to understand your meaning at times. Don\'t worry, with more practice, you\'ll start putting things together more clearly.',
                'You could say a few things, but it wasn\'t a complete response. There were lots of errors in grammar and vocabulary. Keep working on forming full sentences and using a wider range of words — you\'ll get there.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 3.5:
            # List of potential feedback
            potential_feedback = [
                'You gave a few answers, but they were short and often incomplete. It was hard to follow your thoughts because there were lots of pauses. You\'ve got the basics, just keep practicing to build your confidence and fluency.',
                'You made an attempt to speak, but there were many gaps in your sentences. The meaning was often unclear, and you hesitated a lot. Keep working on your grammar and vocabulary so you can communicate more smoothly.',
                'Your response was limited, and the sentences weren\'t fully formed. We could understand bits and pieces, but not everything. Keep practicing and try to speak in longer, more connected sentences next time.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 3.0:
            # List of potential feedback
            potential_feedback = [
                'You gave short answers, but it wasn\'t really a full conversation. Most of what you said was incomplete and difficult to understand. You\'ve got potential, just keep practicing and try to build full sentences.',
                'You said a few words in English, but they didn\'t connect into proper sentences. The meaning wasn\'t clear, and there were a lot of gaps in your response. No worries, with more practice, you\'ll get better at forming complete thoughts.',
                'Your answer was very limited, with lots of pauses and incomplete ideas. It was hard to understand your message, but you tried. Keep working on your vocabulary and grammar to make your responses clearer.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 2.5:
            # List of potential feedback
            potential_feedback = [
                'You said a few words, but it didn\'t form a complete answer. There were long pauses, and it was hard to understand what you were trying to say. Keep practicing, and remember, every attempt helps you get better.',
                'You made some effort, but it was hard to follow what you meant. There were lots of grammar mistakes, and it didn\'t really make sense. It\'s okay — you\'re still in the learning process, just keep pushing forward.',
                'You said a few things in English, but most of it wasn\'t clear enough to understand fully. There was no real structure to your answer. That\'s okay, practice and consistency will help you get more comfortable next time.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 2.0:
            # List of potential feedback
            potential_feedback = [
                'You said a few English words, but they didn\'t form a full sentence. Most of what you said didn\'t really answer the question. You\'re trying, and that\'s what matters — just keep practicing every day.',
                'There was an attempt to speak English, but it was super limited. The words didn\'t really connect, and your meaning wasn\'t clear. It felt like you weren\'t quite sure what to say or how to say it.',
                'You gave some words here and there, but we couldn\'t understand your message. There were no full sentences, and your pronunciation made it tricky. Don\'t stress — small steps forward still count.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 1.5:
            # List of potential feedback
            potential_feedback = [
                'You said a few English words, but they didn\'t really come together into a full sentence. Most of what you said was unclear, and it didn\'t match the questions. That\'s okay — you\'re still super early in your English-speaking journey. Keep practicing little by little!',
                'It felt like you memorized a couple of phrases, but they didn\'t fit the context or meaning. You gave something, but it wasn\'t enough to count as a conversation. With more speaking practice, you\'ll gain the confidence to express real thoughts next time.',
                'We could hear the effort, and that\'s a great first step. But there wasn\'t much connection between your words or ideas. It didn\'t really form a proper answer. No worries — everyone has to start somewhere, and practice will level you up!',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 1.0:
            # List of potential feedback
            potential_feedback = [
                'You said maybe one or two English words, but there wasn\'t enough to understand what you meant. There was no real sentence or clear message. It seemed like you weren\'t able to respond in English yet — and that\'s totally okay. Everyone starts somewhere.',
                'Your response was extremely limited — just a word or two with no structure. It didn\'t form a sentence, and it wasn\'t possible to tell what you were trying to say. Don\'t worry though, speaking takes time. Keep practicing and try again when you\'re ready.',
                'We heard a tiny bit of English, but there was no communication. It might\'ve been a memorized word or phrase, but it didn\'t fit the question. You\'re at the very beginning of your English journey — keep going, even small steps count.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        elif overall_band >= 0.5:
            # List of potential feedback
            potential_feedback = [
                'You tried to say something, but it wasn\'t in English, so we couldn\'t really assess it. It\'s totally okay to feel unsure or blank out — it happens. Next time, even a few English words can make a difference.',
                'We noticed some effort, maybe a few sounds or words, but none of it was English. That means we couldn\'t give a proper score. Don\'t worry — just showing up is a start. Practice a bit more and you\'ll be ready to speak next time.',
                'You gave a response, but it wasn\'t in English or wasn\'t understandable as English. That\'s why this score was given. Take it as a learning step — even saying one English sentence next time would move you up.',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)
        else:
            # List of potential feedback
            potential_feedback = [
                'It looks like you didn\'t say anything during the test. Maybe you were nervous, or something went wrong — and that\'s okay. Just remember, we need to hear you speak to give a score.',
                'No response was given, so we couldn\'t evaluate your English. If you\'re feeling shy or unsure, don\'t stress — next time, just give it a shot. Everyone starts somewhere!',
                'You didn\'t speak at all during the test. It\'s totally fine to be nervous, but to get a score, we need to hear you try. You\'ve got this — don\'t be afraid to speak up next time!',
            ]

            # Randomly select feedback from the list
            overall_feedback = random.choice(potential_feedback)

        # Add html tags to the feedback
        overall_feedback = f'<p>{overall_feedback}</p>'

        # Get fluency feedback
        fluency_feedback = ''

        # Mapping feedback based on the average fluency bands
        if fluency_band >= 9.0:
            # List of potential feedback
            potential_feedback = [
                'Your speech was exceptionally fluent, with no noticeable hesitation or pauses. You spoke naturally and smoothly throughout, making your responses sound confident and professional. There were no awkward pauses, and you maintained a steady flow of speech.',
                'You delivered your responses with high fluency, speaking naturally without any significant pauses. Your ideas were well connected, and you never struggled to find the right words. You spoke with ease, showing complete confidence and comfort with the language.',
                'Your fluency was perfect, with no noticeable pauses or hesitations. You spoke smoothly and consistently, delivering detailed responses without interruptions. Your pace and clarity were excellent, and it was easy to follow your ideas throughout.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 8.5:
            # List of potential feedback
            potential_feedback = [
                'You spoke very fluently with very few pauses, and your ideas were well connected. There were only occasional hesitations, but they didn\'t interrupt the flow of your speech. Your delivery was smooth and confident, making it easy to follow your answers.',
                'Your fluency was strong, with natural speech and minimal pauses. There were only a few moments where you hesitated slightly, but it didn\'t affect your overall fluency. You spoke confidently and clearly, making your responses easy to understand.',
                'You delivered your responses fluently and with very few pauses. While there were a couple of slight hesitations, they didn\'t impact the overall flow of your speech. You maintained a steady pace, and your ideas were communicated smoothly.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 8.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was excellent, with only minor pauses. You spoke clearly and confidently, maintaining a smooth flow for the most part. While there were a few slight hesitations, your responses were generally natural and easy to follow.',
                'Your responses were fluent with good flow and natural pace. There were only occasional pauses, but they didn\'t affect your ability to communicate clearly. Your speech was easy to understand and you maintained good control over the rhythm of your delivery.',
                'You spoke with good fluency, and there was only a minor hesitation here and there. Your ideas were connected well, and there were no long pauses or disruptions. Your speech felt comfortable and natural.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 7.5:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was generally good, but there were occasional pauses and hesitations. Your speech flowed smoothly for the most part, but there were moments where you struggled to find the right words or connect your ideas. Keep practicing for a more consistent flow.',
                'You spoke fairly fluently, though there were some brief pauses as you searched for the right words. Your responses were mostly smooth, but a couple of times you seemed to hesitate or lose track. Focus on building a more natural flow in your responses.',
                'Your speech was generally fluent, but there were a few pauses that slightly interrupted the flow. You were able to get your ideas across, but at times there were small breaks in your speech. Keep practicing to reduce those moments of hesitation.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 7.0:
            # List of potential feedback
            potential_feedback = [
                'You spoke reasonably fluently, but there were frequent pauses as you tried to find the right words or form your sentences. Your speech was clear, but the flow was sometimes interrupted by hesitations. Keep practicing to build a more consistent rhythm and flow.',
                'Your fluency was acceptable, but you hesitated often as you searched for words or connected your ideas. Your responses were still understandable, but they lacked a smooth flow at times. Focus on reducing these pauses to make your speech feel more natural.',
                'You had a clear structure, but there were noticeable pauses and hesitations. The flow of your speech was affected by these breaks, but your message was still understandable. Keep practicing to improve the rhythm and flow of your responses.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 6.5:
            # List of potential feedback
            potential_feedback = [
                'You were able to speak at a reasonable pace, but there were frequent pauses as you looked for words. Your speech was not as smooth as it could be, and there were times when your ideas weren\'t fully connected. Keep practicing to reduce these pauses and improve the natural flow.',
                'Your fluency was acceptable, but you often paused or hesitated as you searched for words. This affected the smoothness of your speech, and your responses were sometimes less connected. More practice with speaking will help you reduce these pauses.',
                'Your speech had frequent breaks, and you sometimes struggled to find the right words. While your responses were understandable, the flow was interrupted too often. Focus on building more fluid speech and connecting your ideas more smoothly.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 6.0:
            # List of potential feedback
            potential_feedback = [
                'You were able to speak, but there were many pauses and hesitations. Your speech lacked a smooth flow and sometimes it felt disjointed. Keep working on reducing these pauses to speak more naturally and with greater confidence.',
                'Your fluency was limited, with frequent pauses and long gaps in your speech. It was hard to follow your responses at times because your thoughts weren\'t connected clearly. Try practicing with full sentences and focusing on fluency to improve your delivery.',
                'You struggled with fluency, often pausing to search for words. There were frequent hesitations that affected the flow of your speech. More practice will help you reduce these pauses and improve the natural rhythm of your speech.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 5.5:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was limited, and there were frequent pauses. Your speech felt disconnected and it was often hard to follow your ideas because you struggled to find the right words. Keep practicing to build more fluid responses.',
                'You paused often, and your ideas didn\'t flow well together. The frequent hesitation made your speech harder to follow. Focus on speaking more confidently without worrying too much about the exact words.',
                'You tried to speak fluently, but there were a lot of pauses. Your responses weren\'t always clear due to gaps in speech, making it hard to follow your thoughts. Practice speaking in full sentences with more confidence.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 5.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was slow and interrupted by frequent pauses. You hesitated quite a bit, and it made your speech feel disjointed. Keep practicing speaking more continuously to avoid breaking up your thoughts.',
                'You spoke with a lot of hesitation, and it was hard to follow your ideas because of the long pauses. Your fluency was inconsistent, and you struggled to find the right words. Keep working on speaking without interruptions.',
                'There were frequent long pauses in your speech that affected the flow. Your responses were not fluid, and it was hard to follow your thoughts. More practice will help you reduce these pauses and speak more naturally.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 4.5:
            # List of potential feedback
            potential_feedback = [
                'You spoke in short bursts with many pauses, making your fluency difficult to follow. Your ideas were broken up, and it was hard to understand your full response. Focus on practicing fluid speech to connect your ideas more clearly.',
                'Your fluency was poor, with many pauses interrupting your speech. You struggled to connect your ideas and there were long gaps in your responses. More practice will help you speak without pausing too much.',
                'There were constant breaks in your speech, and you often hesitated. This made it hard to understand your responses. Keep practicing to reduce these pauses and improve your fluency.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 4.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was very limited, with constant pauses and broken speech. Your responses were unclear because you struggled to find the right words. Keep working on forming full sentences without interruptions.',
                'You paused repeatedly, and your speech was often hard to follow. The frequent hesitations disrupted the flow of your response. More practice is needed to improve fluency and reduce long pauses.',
                'You struggled with fluency, and your speech was very choppy. You hesitated frequently, making it hard to understand what you were trying to say. Keep practicing to reduce pauses and speak more continuously.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 3.5:
            # List of potential feedback
            potential_feedback = [
                'You spoke in short, disconnected phrases with frequent pauses. It was very difficult to understand your ideas because of the long gaps in your speech. You need a lot more practice to improve your fluency.',
                'Your fluency was very poor, and your speech was broken up by many hesitations. It was hard to follow your answers due to frequent pauses. Keep working on speaking in complete sentences without pauses.',
                'You struggled a lot with fluency, and your speech was interrupted by constant hesitations. This made it very hard to follow your ideas. Keep practicing to speak more smoothly and confidently.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 3.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was very limited, and your speech was almost constantly interrupted by pauses. It was difficult to understand your response because of the long breaks. Focus on speaking without hesitation to improve your fluency.',
                'You had frequent pauses that made your response hard to follow. You struggled to connect your ideas, and the breaks in your speech were very noticeable. Keep practicing to improve fluency and reduce hesitations.',
                'Your fluency was minimal, with constant pauses that interrupted your response. It was hard to understand what you were saying because of the frequent hesitations. Practice speaking continuously to improve your fluency.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 2.5:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was very poor, with long pauses and broken speech. It was hard to follow your ideas because you hesitated a lot. Focus on practicing to speak more fluidly and reduce long pauses.',
                'You hesitated constantly, and your speech was very choppy. It was difficult to understand your meaning because you struggled to connect your thoughts. More practice is needed to improve fluency.',
                'Your speech was interrupted by frequent long pauses. It was difficult to follow what you were saying, and your response felt disconnected. Practice speaking in full sentences to improve fluency.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 2.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was very limited and broken. There were long pauses and it was hard to understand your responses because of constant hesitations. You need to work on speaking more fluidly and without so many pauses.',
                'You struggled to speak continuously, and your responses were very fragmented. The pauses interrupted the flow, making it hard to follow your speech. Focus on practicing without pauses to improve fluency.',
                'Your fluency was minimal, and there were constant breaks in your speech. It was difficult to understand your ideas because of frequent pauses. Keep practicing to speak more naturally and with less hesitation.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 1.5:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was almost non-existent, with constant interruptions and pauses. Your speech was very hard to follow because of the long gaps. You need to practice speaking without breaks to improve fluency.',
                'You struggled with fluency throughout, and there were too many pauses in your speech. It was very difficult to understand your ideas because of the long hesitations. More practice is needed to speak without hesitation.',
                'Your response was heavily interrupted by long pauses. The flow of your speech was poor, and your message was unclear. You need to practice reducing pauses and hesitations.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 1.0:
            # List of potential feedback
            potential_feedback = [
                'Your fluency was almost nonexistent. You struggled to speak and there were long gaps in your responses. It was hard to follow anything you said, and your speech was disconnected.',
                'You hesitated so much that it was nearly impossible to follow your ideas. There were constant long pauses, and your fluency was very poor. More practice is needed to speak without hesitation.',
                'Your speech was very fragmented with constant pauses and no clear flow. It was extremely difficult to understand your message. You need to work on reducing breaks and hesitations.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        elif fluency_band >= 0.5:
            # List of potential feedback
            potential_feedback = [
                'Your speech was almost completely broken and unintelligible due to long pauses and hesitations. It was very difficult to understand anything you said. You need significant practice to improve fluency.',
                'There were too many breaks in your speech, and it was almost impossible to follow your ideas. You need to focus on reducing pauses and improving fluency.',
                'Your fluency was very poor, and your speech was almost unintelligible due to constant pauses. It was hard to follow what you were trying to say, and you need to practice speaking without hesitation.',
            ]

            # Randomly select feedback from the list
            fluency_feedback = random.choice(potential_feedback)
        else:
            # General feedback
            fluency_feedback = 'No feedback available.'

        # Add html tags to the feedback
        fluency_feedback = f'<p>{fluency_feedback}</p>'

        # Get grammar feedback
        grammar_feedback = ''

        # Mapping feedback based on the average grammar bands
        if grammar_band >= 9.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar usage was flawless. You demonstrated a complete command of the language, using a wide range of grammatical structures accurately and effectively. There were no errors in your sentences, and your grammar was diverse and appropriate for the task.',
                'You used complex and varied grammatical structures accurately throughout your responses. There were no mistakes, and your grammar was used confidently and effectively. Your sentences were perfectly constructed, with excellent control of tenses and sentence types.',
                'Your grammar was impeccable, with a wide range of complex structures used appropriately. Every sentence was clear and well-formed, and you made no grammatical errors. Your use of grammar was varied and precise, showing a high level of language proficiency.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 8.5:
            # List of potential feedback
            potential_feedback = [
                'You displayed a strong grasp of grammar with only a few minor errors. Complex structures were used accurately and appropriately, and your sentence construction was varied and correct for the most part.',
                'Your grammar was very good, with only occasional minor mistakes. You used a variety of tenses and sentence types, and your grammar was appropriate to the context. You made few errors, and they didn’t hinder the clarity of your ideas.',
                'Your grammar was excellent, with just a couple of minor errors. You used a range of complex sentence structures with mostly accurate tense usage. While some minor mistakes appeared, they did not detract from the clarity or accuracy of your communication.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 8.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was solid, and you used a wide variety of structures. While there were some minor mistakes, they did not interfere with understanding your responses. You handled complex structures well and demonstrated good grammatical range.',
                'You used a variety of grammatical structures with good accuracy. There were occasional errors, but they were mostly minor and didn’t affect the clarity of your speech. Overall, your grammar use was strong and effective.',
                'Your grammar was mostly accurate, with a mix of simple and complex sentences. You made occasional errors, but they did not affect the communication of your ideas. Keep working on perfecting your grammatical accuracy.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 7.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was good overall, but there were several noticeable errors. You used a range of sentence types, but some of your complex structures were used incorrectly. Some mistakes affected clarity, but they were not too frequent.',
                'You demonstrated a good understanding of grammar, but some errors were evident, especially with more complex structures. Despite the mistakes, your communication remained effective, and you showed a fair control of grammar.',
                'Your grammar was mostly accurate, but you made some errors with sentence structure and tense usage. You attempted complex sentences but occasionally used them incorrectly. Overall, the grammar was good but needs improvement.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 7.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was mostly correct, but you made noticeable errors in sentence structure and verb tense usage. These mistakes affected clarity at times, but you were still able to express your ideas effectively.',
                'You used simple and some complex structures with varying degrees of accuracy. There were errors in verb tenses and sentence construction, which impacted the clarity of some of your responses.',
                'While your grammar was understandable, you made frequent errors in sentence construction and tense use. These mistakes caused some confusion, but overall you were still able to communicate your ideas clearly.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 6.5:
            # List of potential feedback
            potential_feedback = [
                'You made frequent grammar mistakes, particularly with sentence structure and verb tenses. Despite these errors, you were able to get your point across, but the grammar issues made your responses harder to follow.',
                'Your grammar was limited, with many errors in sentence formation, tenses, and article usage. While your speech was still understandable, these errors affected the clarity of your answers.',
                'Your grammar was inconsistent, with noticeable mistakes in almost every sentence. The errors impacted the flow of your speech, and you need to improve your control over grammatical structures to make your speech clearer.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 6.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was weak, with consistent mistakes in basic sentence structures, tenses, and articles. These errors made it difficult to follow your responses at times, but you were still able to express your ideas.',
                'You made frequent errors with basic grammar rules, especially with tenses and sentence structure. While your responses were understandable, these grammar issues impacted the overall clarity and accuracy of your speech.',
                'Your grammar was inconsistent and caused frequent communication breakdowns. You made basic mistakes with sentence structure and verb tenses, which disrupted the flow of your responses.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 5.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was very limited, with frequent errors that made your speech difficult to follow. You made basic mistakes in verb tenses, sentence structure, and word forms. You need to work on improving your grammatical accuracy.',
                'Your responses were full of grammatical mistakes, especially with verb tenses and sentence structure. These errors caused confusion and affected the clarity of your speech.',
                'There were many basic grammar errors throughout your responses. These mistakes made it hard to understand your ideas at times, and you need to focus on improving your use of basic grammar structures.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 5.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was quite weak, with major issues in sentence structure and verb tense use. The frequent errors made your speech difficult to understand at times.',
                'You made many basic grammar mistakes, which caused confusion and affected your fluency. Your sentences were incomplete or incorrect, making it hard to follow your responses.',
                'Your grammar was inconsistent, with numerous mistakes in sentence formation and tenses. These errors made your speech hard to follow, and you need to focus on improving your basic grammar.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 4.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was very limited, and you made frequent errors in basic sentence structures and verb usage. It was often hard to understand your speech due to these mistakes.',
                'You made many basic errors that affected the clarity of your speech. Your sentence structures were often incorrect, and your verb tenses were frequently wrong.',
                'There were many mistakes in your grammar, especially with sentence structure and verb tense use. These errors made it difficult to follow your responses and affected their clarity.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 4.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was very weak, with constant mistakes in basic sentence structure and verb tenses. These errors made your speech difficult to understand and follow.',
                'You made frequent and noticeable errors in grammar, especially with tenses and sentence construction. Your responses were often unclear and difficult to follow because of these mistakes.',
                'Your grammar was basic and error-prone. You struggled with basic sentence structures and verb tenses, making your speech difficult to follow and understand.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 3.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was almost completely incorrect. You made serious errors in every sentence, and it was very hard to understand your ideas.',
                'There were almost constant mistakes in your grammar. Your sentence structure was wrong, and your use of tenses was very limited, which made your speech very difficult to follow.',
                'Your grammar was almost non-existent, with frequent and major errors. This made your speech very difficult to understand, and you need a lot of improvement in this area.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 3.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was extremely poor. There were major mistakes in every sentence, and your speech was very hard to follow due to constant errors.',
                'Your grammar was almost entirely incorrect, with basic mistakes in every response. It was very difficult to understand anything you said because of these errors.',
                'There were constant and serious errors in your grammar, making your speech very difficult to understand. You need extensive practice to improve your basic grammar.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 2.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was almost completely incorrect. You struggled with every basic sentence structure, and your speech was almost unintelligible.',
                'You made constant and major mistakes in every sentence, and your speech was very hard to follow. You need significant improvement in your grammar.',
                'Your grammar was so limited that it was very hard to understand your ideas. You need extensive practice to improve your grammar and make your speech more coherent.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 2.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was completely incorrect. You made serious mistakes in every response, and your speech was incomprehensible.',
                'You made constant errors in every sentence, making it impossible to understand your ideas. Your grammar needs significant improvement.',
                'Your grammar was completely flawed, and your speech was very hard to follow due to constant mistakes. You need to improve your basic grammar skills.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 1.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was very poor, with almost no correct sentences. Your speech was almost impossible to understand.',
                'You made so many errors that it was very difficult to follow your speech. There was almost no use of correct grammar.',
                'Your speech was completely disjointed because of the grammar mistakes. You need to focus on learning basic grammar.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 1.0:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was almost non-existent, making it extremely hard to understand your responses.',
                'You made serious mistakes in almost every sentence, making it very difficult to follow your speech.',
                'Your grammar was almost completely wrong, and your speech was impossible to follow.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        elif grammar_band >= 0.5:
            # List of potential feedback
            potential_feedback = [
                'Your grammar was extremely limited. It was almost impossible to understand anything you said.',
                'Your grammar errors were so frequent and serious that it made your speech unintelligible.',
                'You did not use any correct grammar in your response, making it very difficult to understand your ideas.'
            ]

            # Randomly select feedback from the list
            grammar_feedback = random.choice(potential_feedback)
        else:
            # General feedback
            grammar_feedback = 'No feedback available.'

        # Add html tags to the feedback
        grammar_feedback = f'<p>{grammar_feedback}</p>'

        # Get lexical feedback
        lexical_feedback = ''

        # Mapping feedback based on the average lexical resource bands
        if lexical_band >= 9.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was outstanding, with a wide range of sophisticated and precise words used appropriately throughout your responses. You demonstrated a deep understanding of nuances in the language and varied your vocabulary to great effect.',
                'You used a vast array of advanced vocabulary, making your speech sound both natural and fluent. Your choice of words was highly accurate, and you managed to express complex ideas clearly and effectively.',
                'Your lexical resource was exceptional. You used an impressive range of words, demonstrating both depth and accuracy in your vocabulary choices. You applied them seamlessly to convey your ideas, and they enriched your responses.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 8.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was strong, and you used a wide variety of words accurately. While you may have used some simpler words occasionally, your range was still impressive, and your lexical choices were appropriate for the task.',
                'You demonstrated good control over vocabulary, using precise and varied language throughout. There were moments where more complex words could have been used, but overall, your lexical choices were clear and effective.',
                'You used a good range of vocabulary with minor repetition. While you didn’t always use the most advanced words, your choices were appropriate, and your vocabulary added richness to your responses.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 8.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was solid, with a decent range of words used accurately. You managed to convey your ideas well, but there was some repetition, and occasional opportunities for more advanced word choices were missed.',
                'You demonstrated a good use of vocabulary with minor repetition. While your language was generally appropriate, there were a few moments when more specific or advanced words could have improved your responses.',
                'Your vocabulary was varied enough to express your ideas clearly, but there was some limitation in range. Some words were repeated, and you could improve by incorporating a broader variety of terms.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 7.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was adequate, but you relied on a narrow range of words, with some repetition. More variety in your lexical choices would have enhanced the clarity and expressiveness of your answers.',
                'Your lexical resource was limited, and you used basic vocabulary for the most part. While your ideas were clear, you could have benefited from using more varied and precise vocabulary to improve your answers.',
                'Your vocabulary was understandable, but quite basic. You repeated some words and missed opportunities to showcase more advanced lexical choices. Try to expand your vocabulary for more precise and varied expression.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 7.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was fairly basic, with some repetitive word choices. You were able to convey your ideas, but more variety and sophistication in your lexical choices would have made your speech clearer and more interesting.',
                'Your responses were limited in terms of vocabulary. You used simple and basic words, and there was noticeable repetition. Aim to include more advanced or varied vocabulary to make your speech sound more natural and rich.',
                'You used common vocabulary to express your ideas, but your range was limited. There were opportunities for improvement in word choice, as more specific or varied terms could have added depth to your responses.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 6.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was quite basic, with frequent repetition of simple words. While you conveyed your ideas, you could improve by using more varied and precise vocabulary to avoid sounding repetitive.',
                'You demonstrated limited lexical resource, with basic and repetitive vocabulary. Your responses were clear but lacked variety, and incorporating more advanced words would improve your fluency and communication.',
                'Your vocabulary was somewhat repetitive and simple, limiting your ability to express more complex ideas. You need to work on expanding your lexical range to improve the sophistication of your responses.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 6.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was basic and repetitive, with limited range. You struggled to find appropriate words for more complex ideas, and this made your speech sound less fluent and natural.',
                'You used very simple vocabulary, and there was a lot of repetition. You need to expand your vocabulary range and focus on using more varied words to improve the clarity and depth of your responses.',
                'Your vocabulary was restricted, and many words were repeated throughout your responses. Work on expanding your word choices to make your answers more dynamic and diverse.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 5.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was very limited, and you relied heavily on basic words. There was frequent repetition, and you struggled to express more complex ideas due to your limited lexical range.',
                'You used a small range of basic vocabulary, which made your responses feel repetitive. You need to expand your lexical range to improve your ability to communicate more complex ideas clearly.',
                'You demonstrated a very limited vocabulary, and your speech often lacked variety. Focus on learning and incorporating more advanced vocabulary to make your responses sound more natural and fluid.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 5.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was very basic, with little variety. You used simple and repeated words throughout your responses, which limited the clarity of your ideas. Work on expanding your lexical range.',
                'Your responses lacked variety in vocabulary, and many words were used incorrectly or repetitively. You need to significantly improve your vocabulary and learn to use more varied terms.',
                'You struggled with vocabulary, using a small number of basic words. The limited vocabulary made it hard to follow your responses, and you need to practice using more varied and accurate terms.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 4.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was extremely limited, and you used the same words repeatedly. This made your speech very difficult to understand and lacked any variety or depth.',
                'You used a very small set of vocabulary words, and there was excessive repetition. Your speech lacked clarity and richness, and you need to build a wider vocabulary to express ideas more effectively.',
                'Your responses were characterized by poor vocabulary usage and significant repetition. You need to focus on expanding your vocabulary and using a wider range of words to improve your speech.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 4.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was inadequate, with constant repetition and incorrect usage of words. You struggled to express your ideas, and your speech was difficult to understand due to limited word choices.',
                'Your vocabulary was too basic, and you made frequent errors in word choice. The limited vocabulary severely impacted your ability to communicate clearly, and you need to improve your word range.',
                'You used a narrow and repetitive vocabulary, making it difficult to understand your responses. Focus on learning new words and avoiding repetitive usage to improve your lexical range.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 3.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was almost non-existent, with constant repetition of the same words. Your speech was unclear, and you need significant improvement in building your word bank.',
                'You used almost no varied vocabulary, and your speech was very hard to follow. There was major repetition, and you need a lot of practice to improve your lexical range.',
                'Your vocabulary was severely limited, and your responses were almost unintelligible due to lack of variety in word choice. You must work on expanding your vocabulary significantly.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 3.0:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was extremely poor. You used basic words and repeated them constantly. Your speech was difficult to follow, and you need to focus on expanding your vocabulary and avoiding repetition.',
                'You had a very limited vocabulary, which made your responses hard to understand. Your word choices were almost all basic and repetitive, and you need extensive practice to improve your lexical resource.',
                'Your vocabulary was almost entirely incorrect or overly simple. This made it hard to follow your responses, and you need to learn more words to communicate more effectively.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 2.5:
            # List of potential feedback
            potential_feedback = [
                'Your vocabulary was minimal, and your speech was extremely difficult to understand. You used a very limited range of words and need to expand your vocabulary significantly.',
                'You struggled to find the right words and used the same ones repeatedly. Your responses were not clear due to your limited vocabulary, and you need to focus on improving this area.',
                'Your vocabulary was almost entirely incorrect, and you used a very narrow range of words. You need to focus on learning new words and improving your lexical variety.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 2.0:
            # List of potential feedback for Band 1.5
            potential_feedback = [
                'Your vocabulary was extremely limited and almost nonexistent. You used the same basic words repeatedly, which made your responses hard to follow. Focus on expanding your vocabulary and avoiding repetition.',
                'You showed a very basic understanding of vocabulary with little range. Your responses lacked clarity due to constant repetition of simple words. You need to build a larger vocabulary and work on using more precise words.',
                'Your vocabulary was almost entirely wrong or overly simple. You need to work on learning new vocabulary and understanding how to use words more effectively to express your ideas.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 1.5:
            # List of potential feedback for Band 1
            potential_feedback = [
                'Your vocabulary was extremely basic and repetitive, making it difficult to understand your responses. You need to significantly expand your vocabulary and avoid repeating words over and over.',
                'You used only a handful of simple words, and there was no variety in your vocabulary. This made your speech hard to follow, and you should focus on learning new words and phrases.',
                'Your vocabulary was almost nonexistent, with very little range. Your responses were unclear due to the lack of vocabulary variety, and you need to dedicate time to improving your lexical resource.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 1.0:
            # List of potential feedback for Band 0.5
            potential_feedback = [
                'Your vocabulary was severely limited, with almost no variety or depth. You used very basic and incorrect words, making your responses unintelligible. You need to work on building a more comprehensive vocabulary.',
                'Your vocabulary was so limited that it was almost impossible to understand your responses. You need to work on expanding your vocabulary and avoid using the same words repetitively.',
                'The vocabulary you used was almost nonexistent, and your responses were extremely difficult to follow. You need to focus on learning new words and improving your basic understanding of vocabulary.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        elif lexical_band >= 0.5:
            # Default feedback for Band 0
            potential_feedback = [
                'Your vocabulary was non-existent, and you did not manage to communicate any clear ideas. You need to start building your vocabulary from the basics and work on using more words to express yourself.',
                'Your responses were completely unclear due to the lack of any recognizable vocabulary. Start by learning the most basic words and try to practice them in different contexts.',
                'There was no vocabulary used that was understandable. You need to focus on learning a basic set of words and work on using them correctly in order to express yourself more clearly.'
            ]
            # Randomly select feedback from the list
            lexical_feedback = random.choice(potential_feedback)
        else:
            # General feedback
            lexical_feedback = 'No feedback available.'

        # Add html tags to the feedback
        lexical_feedback = f'<p>{lexical_feedback}</p>'

        # Get pronunciation feedback
        pronunciation_feedback = ''

        # Pronunciation feedback based on the band
        if pronunciation_band >= 9.0:
            # List of potential feedback for Band 9
            potential_feedback = [
                'Your pronunciation was flawless, with clear and accurate pronunciation of every word. There was no noticeable accent, and your speech was easy to understand at all times.',
                'Your pronunciation was perfect, with clear intonation and stress patterns. You enunciated each word clearly, and your accent did not hinder communication at all.',
                'Your pronunciation was outstanding, with natural intonation, stress, and rhythm. There were no issues with any sounds, and your speech was smooth and easy to follow throughout.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 8.5:
            # List of potential feedback for Band 8.5
            potential_feedback = [
                'Your pronunciation was very clear with only occasional minor mispronunciations. The rhythm and intonation were natural, and your accent did not interfere with understanding.',
                'Your pronunciation was strong, with clear and accurate sounds. There were very few mispronunciations, and overall, your speech was easy to understand and pleasant to listen to.',
                'Your pronunciation was very good, with minor issues in stress or intonation. However, your speech was generally clear, and your accent did not affect communication.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 8.0:
            # List of potential feedback for Band 8
            potential_feedback = [
                'Your pronunciation was clear, with only occasional errors in specific sounds. Your intonation and rhythm were mostly correct, and it was easy to understand your speech.',
                'Your pronunciation was generally good, with a few slight mispronunciations. These didn\'t affect your overall clarity, but you may want to focus on specific sounds or stress patterns.',
                'Your pronunciation was quite clear, but you made some small mistakes with certain sounds or word stress. Overall, it was easy to follow your speech.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 7.5:
            # List of potential feedback for Band 7.5
            potential_feedback = [
                'Your pronunciation was quite clear, but you occasionally mispronounced words. The rhythm and intonation were generally correct, but there were moments where it was harder to understand.',
                'Your pronunciation was mostly clear, with a few noticeable mispronunciations. While you were understandable most of the time, some words could have been pronounced more clearly.',
                'You had a good overall pronunciation, but certain words were mispronounced or unclear. Your rhythm and stress were generally fine, but focus on improving some specific sounds.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 7.0:
            # List of potential feedback for Band 7
            potential_feedback = [
                'Your pronunciation was generally good, but there were several mispronunciations that made parts of your speech harder to follow. You should work on improving your pronunciation of certain sounds.',
                'Your pronunciation was understandable, but you made frequent mispronunciations. It would help if you focused on specific vowels or consonants to improve clarity.',
                'You showed good rhythm and stress patterns, but mispronunciations affected your overall clarity. Focus on practicing certain sounds and word endings to improve your speech.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 6.5:
            # List of potential feedback for Band 6.5
            potential_feedback = [
                'Your pronunciation was understandable but sometimes unclear due to mispronounced words. The rhythm and stress were somewhat inconsistent, which made some parts of your speech hard to follow.',
                'Your pronunciation was okay, but there were frequent mispronunciations that made it harder to understand your ideas. Focus on practicing sounds that are tricky for you.',
                'While your pronunciation was clear at times, there were noticeable errors that made parts of your speech hard to follow. Pay attention to how you pronounce specific words and syllables.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 6.0:
            # List of potential feedback for Band 6
            potential_feedback = [
                'Your pronunciation was generally understandable, but there were several consistent mispronunciations that made it difficult to follow your speech at times.',
                'While your speech was mostly understandable, frequent pronunciation mistakes made it harder to follow. Work on articulating words more clearly and practice your stress patterns.',
                'Your pronunciation made your speech understandable, but frequent mispronunciations caused confusion. Focus on improving clarity and practicing word stress.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 5.5:
            # List of potential feedback for Band 5.5
            potential_feedback = [
                'Your pronunciation was often unclear, and frequent mispronunciations made it hard to understand many of your words.',
                'You made a lot of pronunciation errors, which impacted the clarity of your speech. It’s important to focus on practicing your sounds and word stress to improve understanding.',
                'Your pronunciation was hard to follow at times due to consistent errors. You should practice articulation and make sure you are pronouncing words correctly.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 5.0:
            # List of potential feedback for Band 5
            potential_feedback = [
                'Your pronunciation was often difficult to understand, with frequent mispronunciations and unclear articulation.',
                'There were many mistakes in your pronunciation, making it challenging to follow your speech. You need to focus on practicing pronunciation, especially for difficult sounds.',
                'Your pronunciation errors made it hard to understand many words. Work on improving articulation and focus on practicing common mispronunciations.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 4.5:
            # List of potential feedback for Band 4.5
            potential_feedback = [
                'Your pronunciation made it very hard to understand your speech due to many errors. Focus on learning the correct articulation of sounds and work on clearer pronunciation.',
                'Frequent pronunciation errors impacted the clarity of your speech. You should start focusing on the basic sounds of English to improve your overall clarity.',
                'Your pronunciation was mostly unclear, making it hard for listeners to follow you. Focus on improving your basic articulation of words and sounds.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 4.0:
            # List of potential feedback for Band 4
            potential_feedback = [
                'Your pronunciation was very unclear, and frequent mispronunciations caused confusion. You need to work on the basics of sound articulation and make your speech clearer.',
                'There were many mispronunciations that made it difficult to follow your speech. Focus on practicing common English sounds and how they should be articulated.',
                'Your pronunciation errors were frequent and made your speech very hard to follow. You need to practice basic sounds and work on making your speech clearer.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 3.5:
            # List of potential feedback for Band 3.5
            potential_feedback = [
                'Your pronunciation was so unclear that it was very difficult to understand your speech. You need to focus on learning basic English sounds and practice articulation.',
                'Frequent mispronunciations made it almost impossible to understand your responses. You need to focus on learning the basics of English pronunciation.',
                'Your speech was almost unintelligible due to frequent pronunciation mistakes. You need to work on basic sound production and clear articulation.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 3.0:
            # List of potential feedback for Band 3
            potential_feedback = [
                'Your pronunciation was very hard to understand, and mispronunciations made communication difficult. You should focus on learning the basic sounds of English.',
                'There were major pronunciation issues that made it almost impossible to understand you. You need to focus on learning and practicing the basics of English sounds.',
                'Your pronunciation made it very hard to follow your speech. You need to work on improving basic articulation and sound production.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 2.5:
            # List of potential feedback for Band 2.5
            potential_feedback = [
                'Your pronunciation made it almost impossible to understand you. Focus on learning and practicing the basic sounds and articulation of English.',
                'Pronunciation errors were so frequent that it was difficult to follow your speech. Start focusing on learning English sounds and how to pronounce them correctly.',
                'Your speech was very unclear, and frequent mispronunciations caused confusion. You need to work on articulating sounds more clearly and practice basic pronunciation skills.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 2.0:
            # List of potential feedback for Band 2
            potential_feedback = [
                'Your pronunciation was extremely unclear, with many mistakes making your speech hard to follow. You need to work on sound production and articulation of words.',
                'It was very difficult to understand your speech due to constant mispronunciations. Focus on practicing basic English sounds and word stress.',
                'You mispronounced many words, making your speech unintelligible. You should focus on basic articulation and work on getting the sounds right.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 1.5:
            # List of potential feedback for Band 1.5
            potential_feedback = [
                'Your pronunciation was extremely difficult to follow due to constant errors in articulation. You need to work on the basics of English pronunciation and sound production.',
                'It was hard to understand your speech due to frequent mispronunciations. You need to work on the pronunciation of basic English sounds to improve clarity.',
                'Your speech was unintelligible because of frequent pronunciation mistakes. Start focusing on learning how to pronounce common English words clearly.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 1.0:
            # List of potential feedback for Band 1
            potential_feedback = [
                'Your pronunciation was so unclear that it was difficult to understand your speech. Focus on learning the basics of sound articulation and how to produce English sounds.',
                'Your pronunciation made it almost impossible to understand what you were saying. You need to work on basic pronunciation skills and clear articulation of sounds.',
                'The mispronunciations in your speech were so frequent that it was hard to follow. Focus on practicing individual sounds and work on your overall pronunciation.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)

        elif pronunciation_band >= 0.5:
            # List of potential feedback for Band 0.5
            potential_feedback = [
                'Your pronunciation was almost impossible to understand due to serious mistakes. You need to work from the very basics of pronunciation.',
                'Your speech was unintelligible due to mispronunciations. Start with practicing basic sounds and articulation to improve your clarity.',
                'The mispronunciations in your speech made it extremely hard to follow. You need to start practicing basic sounds and pronunciation skills.'
            ]
            # Randomly select feedback from the list
            pronunciation_feedback = random.choice(potential_feedback)
        else:
            # General feedback
            pronunciation_feedback = 'No feedback available.'

        # Add html tags to the feedback
        pronunciation_feedback = f'<p>{pronunciation_feedback}</p>'

        # Create the overall evaluation model
        overall_evaluation = EvOverallEvaluationModel(
            overall_band = overall_band,
            overall_feedback = overall_feedback,
            fluency_band = fluency_band,
            fluency_feedback = fluency_feedback,
            lexical_band = lexical_band,
            lexical_feedback = lexical_feedback,
            grammar_band = grammar_band,
            grammar_feedback = grammar_feedback,
            pronunciation_band = pronunciation_band,
            pronunciation_feedback = pronunciation_feedback,
        )

        # Return the overall evaluation model
        return overall_evaluation

# MARK: OverallFeedbackServiceInstance
# Create the overall feedback service instance
overall_feedback_service = OverallFeedbackService()