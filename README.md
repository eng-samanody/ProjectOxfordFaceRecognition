#Microsoft Cognitive Services (formerly ProjectOxford Ai) Face Recognition

face recognition client wrapper
===================================================
This repo contains the python example that demonstrate Microsoft’s cloud-based face recognition algorithms designed to Detect human faces and compare similar ones, organize people into groups according to visual similarity, and identify previously tagged people in images. major functions will include :

Face Detection    
--------------
Detect one or more human faces in an image and get back face rectangles for where in the image the faces are, along with face attributes which contain machine learning-based predictions of facial features.  After detecting faces, you can take the face rectangle and pass it to the Emotion API to speed up processing. The face attribute features available are: Age, Gender, Pose, Smile, and Facial Hair along with 27 landmarks for each face in the image.  Try this now by uploading a local image, or providing an image URL. We don’t keep your images for this demo unless you give us permission.        

Face Identification
-------------------
Search and identify faces. Tag people and groups with user-provided data and then search those for a match with previously unseen faces.

Requirements
------------
you will need subscription key to be able to use that wrapper
to get one sign in with microsoft account to : https://www.microsoft.com/cognitive-services/en-US/subscriptions
and look for "Face - Preview"
