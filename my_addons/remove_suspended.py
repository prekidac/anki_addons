from aqt.main import AnkiQt
import subprocess


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        sus_nid = self.col.db.list(
            "select nid from cards where queue == -1 group by nid")
        remove_nids = []
        num_of_del = 0
        for nid in sus_nid:
            nid_queues = self.col.db.list(
                "select queue from cards where nid == ?", nid)
            for queue in nid_queues:
                if queue != -1:
                    break
            else:
                num_of_del += len(nid_queues)
                remove_nids.append(nid)
        self.col.remove_notes(remove_nids)
        p = subprocess.Popen(["efficiency", "-a", f"{num_of_del}"])
        p.wait()
        if num_of_del:
            print("Removed:", num_of_del, "cards")
        return func(self)
    return wrapper


AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)
