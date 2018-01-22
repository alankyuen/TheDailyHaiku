import boto3
import json
s3 = boto3.resource('s3')
polly = boto3.client('polly')
response = polly.synthesize_speech(
    OutputFormat='mp3',
    Text='two hundred of their,, rowings entires enoughs,, in their first chancer',
    VoiceId='Emma'
)
with open('output.mp3','wb') as f:
    f.write(response['AudioStream'].read())
    f.close()

"""
comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')

text = "It is raining today in Seattle"
"Amazon.com, Inc. is located in Seattle, WA and was founded July 5th, 1994 by Jeff Bezos, allowing customers to buy everything from books to blenders. Seattle is north of Portland and south of Vancouver, BC. Other notable Seattle-based companies are Starbucks and Boeing."
print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')

"""
"""
amazon comprehend
BatchDetectDominantLanguage

BatchDetectEntities

BatchDetectKeyPhrases

BatchDetectSentiment

DescribeTopicsDetectionJob

DetectDominantLanguage

DetectEntities

DetectKeyPhrases

DetectSentiment

ListTopicsDetectionJobs

StartTopicsDetectionJob
"""


"""
amazon polly
can_paginate()
delete_lexicon()
describe_voices()
generate_presigned_url()
get_lexicon()
get_paginator()
get_waiter()
list_lexicons()
put_lexicon()
synthesize_speech()
response = client.synthesize_speech(
    LexiconNames=[
        'string',
    ],
    OutputFormat='mp3',
    SampleRate='16000',
    SpeechMarkTypes=[
        'sentence',
    ],
    Text='Long hard rain. Hanging in the willows. Tender new leaves',
    VoiceId=''
)
Parameters
LexiconNames (list) --
List of one or more pronunciation lexicon names you want the service to apply during synthesis. Lexicons are applied only if the language of the lexicon is the same as the language of the voice. For information about storing lexicons, see PutLexicon .

(string) --
OutputFormat (string) --
[REQUIRED]

The format in which the returned output will be encoded. For audio stream, this will be mp3, ogg_vorbis, or pcm. For speech marks, this will be json.

SampleRate (string) --
The audio frequency specified in Hz.

The valid values for mp3 and ogg_vorbis are "8000", "16000", and "22050". The default value is "22050".

Valid values for pcm are "8000" and "16000" The default value is "16000".

SpeechMarkTypes (list) --
The type of speech marks returned for the input text.

(string) --
Text (string) --
[REQUIRED]

Input text to synthesize. If you specify ssml as the TextType , follow the SSML format for the input text.

TextType (string) -- Specifies whether the input text is plain text or SSML. The default value is plain text. For more information, see Using SSML .
VoiceId (string) --
[REQUIRED]

Voice ID to use for the synthesis. You can get a list of available voice IDs by calling the DescribeVoices operation.
"""
