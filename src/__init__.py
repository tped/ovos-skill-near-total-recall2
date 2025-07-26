from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

# import os
# import json
# from datetime import datetime
# import numpy as np
# from sentence_transformers import SentenceTransformer

# NTR data and tuning parameters in <NTR_Skill>/settings.json
DEFAULT_SETTINGS = {
    "embeddings_path": "/home/ovos/NTR-Data/MeePiEmbeddings.npy",
    "memories_data_path": "/home/ovos/NTR-Data/MeePiMemories.json",
    "mee_image_path": "/home/ovos/NTR-Data/cover.jpg",
    "media_folder": "/home/ovos/MeePi_Media",
    "display_mee_image":  True,
    "fallback_friendly": False,  # True to quietly pass unknowns on to AI Brain
    # Tuning parameters (from CONFIG in Python script)
    "top_n": 5,  # Number of top results to return
    "similarity_threshold": 0.32,  # Minimum similarity score to consider a match
    "model_name": "all-MiniLM-L6-v2"  # Embedding model
}


class NearTotalRecallSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().
        """
        super().__init__(*args, **kwargs)
        self.learning = True
        self.is_reciting = False

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=True,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    def initialize(self):
        # merge default settings
        # self.settings is a jsondb, which extends the dict class and adds helpers like merge
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)
        # set a callback to be called when settings are changed
        # self.settings_change_callback = self.on_settings_changed

        # self.load_databanks()
        self.speak("Near Total Recall Stub is up and ready!")
        self.log.info("Done with Initialize - #5")

    def on_settings_changed(self):
        """This method is called when the skill settings are changed."""
        self.log.info("Settings changed!")

    @intent_handler("DoYouRecall.intent")
    def handle_do_you_recall_intent(self, message):
        self.speak("Near Total Recall Test - here's the message")
        self.speak_dialog("I should recall a memory but I'm a stub")
        return

    @intent_handler("MemoryChecker.intent")
    def handle_memory_checker_intent(self, message):
        self.speak("Near Total Recall Memory Checker Test - here's the message")
        self.speak_dialog("I can't remember anything")
        return

    def stop(self):
        """Optional action to take when "stop" is requested by the user.
        This method should return True if it stopped something or
        False (or None) otherwise.
        If not relevant to your skill, feel free to remove.
        """
        if self.is_reciting:
            self.speak("")  # Stop MeePi from talking
            self.is_reciting = False
            self.speak_dialog("stopped_talking.dialog")  # Feedback
            self.log.info("MeePi was interrupted by user.")
            return True  # Indicate that MeePi stopped
        return False  # Nothing was interrupted
