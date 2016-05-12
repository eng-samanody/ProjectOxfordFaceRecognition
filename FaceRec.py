#for more details check out the documentation page :
#https://dev.projectoxford.ai/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236

import httplib, urllib, json, os
from os import listdir
from os.path import isfile, join
from string import split
from os.path import basename


ocp_apim_subscription_key = '**********************' # replace this your supbscription key
core_api_url = 'api.projectoxford.ai'

###########################################################################
def performRequest(request_type, params, body, headers):    
    try:
        conn = httplib.HTTPSConnection(core_api_url)
        conn.request(request_type,  params, body, headers)
        response = conn.getresponse()
        #data = response.read()
        #print(data)
        #conn.close()
        return response
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        

###########################################################################
'''
Face - Detect

- Detect human faces in an image and returns face locations, and optionally with face ID, landmarks, and attributes.
- Optional parameters for returning face ID, landmarks, and attributes. Attributes include age, gender, smile intensity, facial hair and head-pose. 
- Face ID is for other APIs use including Face - Identify, Face - Verify, and Face - Find Similar. The face ID will expire in 24 hours after detection call.
- JPEG, PNG, GIF(the first frame), and BMP are supported. The image file size should be no larger than 4MB.
- The detectable face size is between 36x36 to 4096x4096 pixels. The faces out of this range will not be detected.
- A maximum of 64 faces could be returned for an image. The returned faces are ranked by face rectangle size in descending order.
- Some faces may not be detected for technical challenges, e.g. very large face angles (head-pose) or large occlusion. Frontal and near-    frontal faces have the best results.
- Attributes (age, gender, headPose, smile and facialHair, and glasses) are still experimental and may not be very accurate. HeadPose's pitch value is reserved as 0.

'''
###########################################################################
def detectFaceUrl(image_url=None, face_attributes=None):    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }
    params = "/face/v1.0/detect?%s" % urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': face_attributes, # Attributes (age, gender, headPose, smile and facialHair, and glasses) 
    })    
    body = "{0}\"url\":\"{1}\"{2}".format("{",image_url,"}")
    request_type = "POST"    
    performRequest(request_type, params, body, headers)

###########################################################################    

def detectFaceLocalImage(image_path=None, face_attributes=None):    
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }
    params = "/face/v1.0/detect?%s" % urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': face_attributes,
    })    
    #body = "{0}\"url\":\"{1}\"{2}".format("{",image_url,"}")
    body = open(image_path, "rb").read()
    request_type = "POST"    
    response = performRequest(request_type, params, body, headers)
    response = json.loads(response.read())
    return response
###########################################################################
'''
Person - Create a Person
Create a new person in a specified person group for identify. A newly created person have no registered face, you can call Person - Add a Person Face API to add faces to the person.
The number of persons has a subscription limit. For free subscription, the limit is 1000. 
'''
###########################################################################
def createPerson(person_group_id=None,person_name=None):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }
    params = "/face/v1.0/persongroups/{personGroupId}/persons?%s" % urllib.urlencode({'personGroupId':person_group_id})
    #personGroupId (string) User-provided person group ID as a string. 
    #The valid characters include numbers, english letters in lower case,
    # '-' and '_'. The maximum length of the personGroupId is 64.
    body = "{0}\"name\":\"{1}\"{2}".format("{",person_name,"}")
    request_type = "POST"    
    response = performRequest(request_type, params, body, headers)
    #data = response.read()
    #print data
    response = json.loads(response.read())
    print response["personId"]
    return response["personId"]
###########################################################################
def listAllGroupPersons(person_group_id = None):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }        
    params = "/face/v1.0/persongroups/"+person_group_id+"/persons" 
    body = "{body}"
    request_type = "GET"    
    response = performRequest(request_type, params, body, headers)
    response = json.loads(response.read().decode('utf-8'))
    return response   
###########################################################################    
def deletePerson(person_group_id = None, personId = None):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key ,
    }
    params = "/face/v1.0/persongroups/{personGroupId}/persons/{personId}?%s" % urllib.urlencode( 
    { 
        'personGroupId' : person_group_id ,
        'personId': personId,
    })
    body = "{body}"
    request_type = 'DELETE'  
    performRequest(request_type, params, body, headers)
###########################################################################
'''
Add a Person Face

Add a representative face to a person for identification. The input face is specified as an image with a targetFace rectangle. It returns an persistedFaceId representing the added face and this persistedFaceId will not expire.
    - The persistedFaceId is only used in Face - Identify and Person - Delete a Person Face
    - Each person has a maximum of 248 faces.
    - JPEG, PNG, GIF(the first frame), and BMP are supported. The image file size should be no larger than 4MB.
    - The detectable face size is between 36x36 to 4096x4096 pixels. The faces out of this range will not be detected.
    - Rectangle specified by targetFace should contain exactly one face. Zero or multiple faces will be regarded as an error. Out of detectable face size, large head-pose, or very large occlusions will also result in fail to add a person face.
    - The given rectangle specifies both face location and face size at the same time. There is no guarantee of corrent result if you are using rectangle which are not returned from Face - Detect.

'''
def addPersonLocalImage(image_path = None, person_group_id = None, person_id = None):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }
    params = "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % urllib.urlencode({
        # Request parameters
        'personGroupId': person_group_id, 
        'personId': person_id, 
    })
    body = open(image_path, "rb").read()
    request_type = "POST"    
    performRequest(request_type, params, body, headers)
    
 
###########################################################################
def createPersonGroup(group_name=None,user_data=None,person_group_id=None):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key ,
    }
    params = "/face/v1.0/persongroups/{personGroupId}?%s" %  urllib.urlencode({'personGroupId':person_group_id})
    body = "{0}\"name\":\"{1}\",\"userData\":\"{2}\"{3}".format("{",group_name,user_data,"}")
    request_type = "PUT"
    performRequest(request_type, params, body, headers)
###########################################################################

###########################################################################
def deletePersonGroup(person_group_id=None):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key ,
    }    
    params = "/face/v1.0/persongroups/{personGroupId}?%s" % urllib.urlencode({'personGroupId':person_group_id})
    body = "{body}"
    request_type = "DELETE"
    performRequest(request_type, params, body, headers)
###########################################################################

###########################################################################
def listAllPersonGroups():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key ,
    }
    params = "/face/v1.0/persongroups?%s" % urllib.urlencode({})
    body = "{body}"    
    request_type = "GET"
    response = performRequest(request_type, params, body, headers)
    response = json.loads(response.read())
    #print response
    return response

def getPersonId(person_group_id,person_name):
    person_id = None
    response = listAllGroupPersons(person_group_id)
    if len(response) > 0 :
        for i in range(len(response)):
            if response[i]['name']  == person_name:
                person_id =  response[i]['personId']
    return person_id

def createModelFromLocalImages(person_name,person_group_id):
    input_path = os.path.join(os.path.dirname(__file__),os.pardir)
    input_path = os.path.join(input_path,"models/{}/".format(person_name))
    input_image_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    #image_path = (input_path + input_image_files[0])
    #persons_id_list
    person_id =  getPersonId(person_group_id,person_name)                            
    for x in range(len(input_image_files)):
            image_path = input_path + input_image_files[x]
            parts = split(basename(image_path),'.')
            extn = parts[len(parts) - 1]
            if (extn == 'png' or extn == 'jpg'):              
                addPersonLocalImage(image_path, person_group_id, person_id)

def getPersonGroupTrainingStatus(person_group_id):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }
    
    params = "/face/v1.0/persongroups/{personGroupId}/training?%s" %  urllib.urlencode({ 'personGroupId':person_group_id })
    request_type = "GET"
    body = "body"
    response = performRequest(request_type, params, body, headers)
    response = json.loads(response.read())
    #print response
    return response

def trainPersonGroup(person_group_id):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
    }    
    params = "/face/v1.0/persongroups/{personGroupId}/train?%s" %  urllib.urlencode({ 'personGroupId':person_group_id })
    request_type = "POST" 
    body = "body"
    performRequest(request_type, params, body, headers)
    #response = json.loads(response.read())
    #print response
    #return response
    
def identify(image_path=None, person_group_id=None,max_num_of_candidates_returned=1):
    #check if the image contains faces
    check_result = detectFaceLocalImage(image_path=image_path,face_attributes="gender")
    if (len(check_result)>0): 
        #print json.dumps(check_result)
        face_id = check_result[0]['faceId']
        headers = {
         # Request headers
         'Content-Type': 'application/json',
         'Ocp-Apim-Subscription-Key': ocp_apim_subscription_key,
        }
        params = "/face/v1.0/identify"  
        body =  {
            "personGroupId":person_group_id,
            "faceIds":face_id,
            "maxNumOfCandidatesReturned":max_num_of_candidates_returned 
        }        
        #body = {"personGroupId":"olc", "faceIds":["face_id" ],"maxNumOfCandidatesReturned":2}
        body = "{0}\"personGroupId\":\"{1}\", \"faceIds\":[\"{2}\" ],\"maxNumOfCandidatesReturned\":1{3}".format("{",person_group_id,face_id,"}")
        request_type= "POST"
        response = performRequest(request_type,  params, body, headers)
        response = json.loads(response.read())
        #identity = getPersonName(  , 'olc')
        if len(response) > 0 :    
            person_id = response[0]['candidates'][0]['personId']
            person_name = json.dumps(getPersonName( person_id , person_group_id))
            return person_name
        else :
            return None

def getPersonName(person_id=None,person_group_id=None):
    response = listAllGroupPersons(person_group_id)
    #print len(response)
    for person in response:
        if person['personId'] == person_id:
            name = person['name']
            return name
        
    return None
    
    #print json.dumps(response)
    
#print getPersonName( '***-***-****-***-*****' , 'test')

#url = "http://www.uni-regensburg.de/Fakultaeten/phil_Fak_II/Psychologie/Psy_II/beautycheck/english/durchschnittsgesichter/m%2801-32%29_gr.jpg"

#detectFace(image_url=url,face_attributes="age,gender")

#print detectFaceLocalImage(image_path= "/home/raouf/Desktop/img.jpg" , face_attributes="age,gender")

#print json.dumps(identify(image_path="/home/raouf/Desktop/img2.png", person_group_id='test'))

#createPersonGroup(group_name="TEST",person_group_id="test")

#deletePersonGroup(person_group_id="test")

#createPerson(person_group_id='test',person_name='kandil')


#addPersonLocalImage(image_path = None, person_group_id = None, person_id = None)

#print listAllPersonGroups()
#print json.dumps(listAllGroupPersons('test')[1]['persistedFaceIds'])
#print json.dumps(listAllGroupPersons('test'))

#print json.dumps(getPersonGroupTrainingStatus('test'))


#print getPersonId('test','name')

#createModelFromLocalImages('name','test')

#print json.dumps(getPersonGroupTrainingStatus('test'))
#print trainPersonGroup('test')
