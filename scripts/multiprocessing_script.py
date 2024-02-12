import os
from concurrent.futures import ProcessPoolExecutor
import face_recognition

KNOWN_FACES_DIR = "myapp/Mismatched"

def process_image(image_path):
    try:
        person_image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(person_image)
        if face_encodings:
            return face_encodings[0]
        return None
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def load_known_faces():
    known_faces_dict = {}

    with ProcessPoolExecutor() as executor:
        for person_dir in os.listdir(KNOWN_FACES_DIR):
            person_path = os.path.join(KNOWN_FACES_DIR, person_dir)

            if os.path.isdir(person_path):
                department, mis_number, *name_parts = person_dir.split() 

                person_name = " ".join([mis_number] + name_parts)
                print(person_name)

                image_paths = [os.path.join(person_path, filename) for filename in os.listdir(person_path) if filename.endswith(".jpg")]

                face_encodings = list(executor.map(process_image, image_paths))
                valid_face_encodings = [encoding for encoding in face_encodings if encoding is not None]

                if department not in known_faces_dict:
                    known_faces_dict[department] = {'encodings': [], 'names': []}

                known_faces_dict[department]['encodings'].extend(valid_face_encodings)
                known_faces_dict[department]['names'].extend([person_name] * len(valid_face_encodings))

    return known_faces_dict
if __name__ == '__main__':
 
    known_faces_dict = load_known_faces()

    for key, value in known_faces_dict.items():
        print(f"Key: {key}")
        print(f"Face Encodings: {value['encodings']}")
        print(f"Names: {value['names']}")
        print()
