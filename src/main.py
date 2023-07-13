import os
import shutil
import subprocess
from constant import GIT_REPO_URL, MIDI_FILE_PATH, MAX_LEN, TRAINING_PARAMETERS

def clone_git_repo(git_repo_url):
    subprocess.call(["git", "clone", git_repo_url])

def copy_midi_file(source_path, target_path="."):
    """get MIDI file"""
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file does not exist: {source_path}")
    shutil.copy(source_path, target_path)

def prepare_data():
    """Prepare data from MIDI file."""
    data = []
    with open('midi.txt', 'r') as f:
        for _ in f:
            _ = _.strip()
            s = _.split(' ')
            
            if len(s) > MAX_LEN:
                s = list(reversed(s[:MAX_LEN]))
                for i, x in enumerate(s):
                    if x[0] == 'n':
                        s = s[i:]
                        break
                s = list(reversed(s))

            if len(s) <= MAX_LEN:
                data.append(s)

def tokenize_data():
    """Tokenize data."""
    subprocess.call(["python", "src/utils/custom_tokenizer.py", "train-word-level", "data/midi/midi.txt"])

def split_dataset():
    """Split dataset into training and testing."""
    with open('data/midi/midi.txt', 'r') as file:
        lines = file.read().splitlines()

    train_data = lines[:10000]
    test_data = lines[-997:]

    with open('data/midi-train.txt', 'w') as file:
        file.write('\n'.join(train_data))

    with open('data/midi-test.txt', 'w') as file:
        file.write('\n'.join(test_data))

def update_training_script():
    """Update the training shell script."""
    with open('scripts/run_train.sh', 'r') as file:
        script = file.read()

    script = script.replace('save_interval 10', 'save_interval 100')
    # Uncomment the next line if you need to edit the gaussian_diffusion.py file
    # script = script.replace('model.model.get_', 'model.model.model.get_')

    with open('scripts/run_train.sh', 'w') as file:
        file.write(script)

def run_training(training_parameters):
    """Run training."""
    subprocess.call(training_parameters)

def checkout_file_from_git():
    """Checkout a specific file from git."""
    subprocess.call(["git", "checkout", "0605e632", "src/modeling/predictor/transformer_model.py"])

if __name__ == "__main__":
    clone_git_repo(GIT_REPO_URL)
    os.chdir("text-diffusion")
    copy_midi_file(MIDI_FILE_PATH)
    prepare_data()
    tokenize_data()
    split_dataset()
    update_training_script()
    run_training(TRAINING_PARAMETERS)
    checkout_file_from_git()
