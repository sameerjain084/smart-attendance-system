import cv2
import numpy as np
import sqlite3
from datetime import datetime
import os
import pickle

class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # We need integer IDs for LBPHFaceRecognizer
        self.face_data_file = 'face_data.pkl'
        self.model_file = 'face_model.yml'
        
        self.faces = [] # list of numpy arrays (grayscale face crops)
        self.labels = [] # list of integer labels
        self.user_id_map = {} # map string user_id to int label
        self.int_to_user_id = {} # map int label to string user_id
        self.next_label = 0
        
        self.load_data()

    def load_data(self):
        """Load saved face data and recognizer model"""
        try:
            if os.path.exists(self.face_data_file):
                with open(self.face_data_file, 'rb') as f:
                    data = pickle.load(f)
                    self.faces = data['faces']
                    self.labels = data['labels']
                    self.user_id_map = data['user_id_map']
                    self.int_to_user_id = data['int_to_user_id']
                    self.next_label = data['next_label']
                print(f"✅ Loaded {len(self.faces)} face images")
            
            if os.path.exists(self.model_file):
                self.recognizer.read(self.model_file)
                print("✅ Loaded recognizer model")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.faces, self.labels = [], []
            self.user_id_map, self.int_to_user_id = {}, {}
            self.next_label = 0

    def save_data(self):
        """Save face data and train/save recognizer model"""
        try:
            with open(self.face_data_file, 'wb') as f:
                pickle.dump({
                    'faces': self.faces,
                    'labels': self.labels,
                    'user_id_map': self.user_id_map,
                    'int_to_user_id': self.int_to_user_id,
                    'next_label': self.next_label
                }, f)
            print(f"💾 Saved {len(self.faces)} face images data")
            
            if len(self.faces) > 0:
                self.recognizer.train(self.faces, np.array(self.labels))
                self.recognizer.write(self.model_file)
                print("💾 Trained and saved recognizer model")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def get_face(self, image):
        """Extract face from image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            return None
            
        # Return the largest face
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        return face_roi

    def register_face(self, image, user_id, user_name, image_index=0):
        """Register a new face"""
        try:
            print(f"🔍 Registering face image {image_index + 1} for {user_name} ({user_id})")
            
            face_roi = self.get_face(image)
            
            if face_roi is None:
                print("❌ No face detected in the image")
                return False
                
            if user_id not in self.user_id_map:
                self.user_id_map[user_id] = self.next_label
                self.int_to_user_id[self.next_label] = user_id
                self.next_label += 1
                
            label = self.user_id_map[user_id]
            
            # Add to dataset
            self.faces.append(face_roi)
            self.labels.append(label)
            
            # Save to database (dummy representation since LBPH doesn't use 128D encodings)
            self._save_to_database(user_id, user_name, np.array([label]))
            
            # Save and retrain
            self.save_data()
            
            print(f"🎉 Face successfully registered for {user_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error in register_face: {e}")
            return False

    def _save_to_database(self, user_id, user_name, dummy_encoding):
        """Save face encoding to database"""
        try:
            conn = sqlite3.connect('attendance.db')
            cursor = conn.cursor()
            
            encoding_str = str(dummy_encoding.tolist())
            
            cursor.execute('''
                UPDATE students SET face_encoding = ?, registration_date = datetime('now')
                WHERE id = ?
            ''', (encoding_str, user_id))
            
            conn.commit()
            conn.close()
            print(f"💾 Saved face data to database for {user_name}")
            
        except Exception as e:
            print(f"❌ Database save error: {e}")

    def recognize_face(self, image):
        """Recognize a face in the image"""
        try:
            if len(self.faces) == 0:
                return None, 0
                
            face_roi = self.get_face(image)
            
            if face_roi is None:
                return None, 0
                
            label, distance = self.recognizer.predict(face_roi)
            
            # Distance is usually 0-100 (0 being perfect match). Let's convert to confidence.
            # E.g., confidence = 1.0 - (distance / max_distance)
            # Typically for LBPH, distance < 50 is a good match.
            confidence = max(0.0, 1.0 - (distance / 100.0))
            
            user_id = self.int_to_user_id.get(label)
            
            # 0.6 threshold roughly maps to distance < 40
            return user_id, confidence
                
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return None, 0

    def get_user_encodings_count(self, user_id):
        """Count registered face encodings for a user"""
        if user_id not in self.user_id_map:
            return 0
        label = self.user_id_map[user_id]
        return self.labels.count(label)

    def remove_user_faces(self, user_id):
        """Remove all face encodings for a user"""
        if user_id not in self.user_id_map:
            return
            
        label = self.user_id_map[user_id]
        
        # Filter out faces and labels for this user
        filtered_faces = []
        filtered_labels = []
        for i in range(len(self.labels)):
            if self.labels[i] != label:
                filtered_faces.append(self.faces[i])
                filtered_labels.append(self.labels[i])
                
        self.faces = filtered_faces
        self.labels = filtered_labels
        
        del self.user_id_map[user_id]
        del self.int_to_user_id[label]
        
        self.save_data()
        print(f"🗑️ Removed face data for user {user_id}")