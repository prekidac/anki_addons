from aqt.main import AnkiQt

def unloadProfileAndExit(self) -> None:
    new = self.col.db.first("""select count() from cards where type == 0""")
    with open('/tmp/novih', 'w') as f:
        f.write('pr_kartica=' + str(new[0]))

    # FIXME: execute to all
    all_sus_nid = self.col.db.execute("""select nid from cards where queue == -1 group by nid""")
    today_cid = self.col.db.execute("""select cid from revlog where id > ? """, (self.col.sched.dayCutoff-86400)*1000)
    today_nid = []
    for cid in today_cid:
        today_nid.append(self.col.db.execute(""" select nid from cards where id == ? """, cid[0])[0])
    print(today_cid, today_nid)

    to_sus_nid = []
    for nid in all_sus_nid:
        nid_queues = self.col.db.execute("""select queue from cards where nid == """ + str(nid[0]))
        for queue in nid_queues:
            if queue[0] != -1 or nid in today_nid:
                break
        else:
            to_sus_nid.append(nid[0])
    self.col.remove_notes(to_sus_nid)

    self.unloadProfile(self.cleanupAndExit)

AnkiQt.unloadProfileAndExit = unloadProfileAndExit
