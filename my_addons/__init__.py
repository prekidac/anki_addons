import os
from . import shortcuts         # Enter/Tab review
from . import default_conf      # restore to default configuration
from . import unbury_block      # block unBury button
from . import remove_suspended  # remove notes with all suspended cards
from . import limit             # limit learning to "new_card" number of failed cards
from . import auto_rate_typed_answer
from . import suspend_card      # suspend card if reached max_interval
if os.name == "posix":
    from . import write_stats 
from . import answer_modify     # fail card only once per day, easy card
from . import continue_remove
