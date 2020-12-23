from aqt.main import AnkiQt
import json


def unloadProfileAndExit(self) -> None:
    new = self.col.db.scalar("select count() from cards where type == 0")
    try:
        with open("/tmp/routine.json", "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["new_cards"] = new
    with open("/tmp/routine.json", "w") as f:
        json.dump(routine, f, indent=4)

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
    print("Izbrisano:", num_of_del, "kartica")
    self.col.remove_notes(to_sus_nid)

    self.unloadProfile(self.cleanupAndExit)


AnkiQt.unloadProfileAndExit = unloadProfileAndExit
