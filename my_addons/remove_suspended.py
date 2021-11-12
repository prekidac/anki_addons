from aqt.main import AnkiQt
import subprocess


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        all_sus_nid = self.col.db.list(
            "select nid from cards where queue == -1 group by nid")
        today_cid = self.col.db.list(
            "select cid from revlog where id > ? ", (self.col.sched.dayCutoff-86400)*1000)
        today_nid = []
        for cid in today_cid:
            today_nid.append(self.col.db.scalar(
                "select nid from cards where id == ?", cid))
        to_sus_nid = []
        num_of_del = 0
        for nid in all_sus_nid:
            nid_queues = self.col.db.list(
                "select queue from cards where nid == " + str(nid))
            for queue in nid_queues:
                if queue != -1:
                    break
            else:
                if nid not in today_nid:
                    num_of_del += len(nid_queues)
                    to_sus_nid.append(nid)
        self.col.remove_notes(to_sus_nid)
        p = subprocess.Popen(["efficiency", "-a", f"{num_of_del}"])
        p.wait()
        if num_of_del:
            print("Removed:", num_of_del, "cards")
        return func(self)
    return wrapper


AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)
