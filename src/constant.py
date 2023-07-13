DATA_PATH = "midi_database"
MIN_NOTE_MULTIPLIER = 0.125
MIDI_EXTENSIONS = [".mid", ".midi"]
GIT_REPO_URL = "https://github.com/infinfin/text-diffusion"
MIDI_FILE_PATH = "midi.txt"
MAX_LEN = 128
TRAINING_PARAMETERS = ["python", "-u", "src/train_infer/train.py", "--checkpoint_path", "ckpts/midi", "--log_interval", 
                       "2", "--save_interval", "100", "--lr", "0.0001", "--batch_size", "32", "--diffusion_steps", "2000",
                       "--noise_schedule", "sqrt", "--sequence_len", "130", "--seed", "10708", "--dropout", "0.1", 
                       "--in_channel", "128", "--out_channel", "128", "--weight_decay", "0.0", "--predict_xstart", "True",
                       "--train_txt_path", "data/midi-train.txt", "--dataset", "midi", "--val_txt_path", "data/midi-test.txt",
                       "--num_heads", "4", "--config_name", "bert-base-uncased", "--init_pretrained", "False",
                       "--freeze_embeddings", "False", "--use_pretrained_embeddings", "False",
                       "--notes", "Pre-trained models, pre-trained embeddings, embeddings not frozen", "--lr_anneal_steps", "5000"]
