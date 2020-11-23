from aqt.main import AnkiQt

def unloadProfileAndExit(self) -> None:
    new = self.col.db.first("""select count() from cards where type == 0""")
    with open('/tmp/novih', 'w') as f:
        f.write('pr_kartica=' + str(new[0]))

    all_nid = self.col.db.execute("""select nid from cards
                                  where queue == -1 group by nid""")
    sus_nid = []
    for nid in all_nid:
        nid_queues = self.col.db.execute("""select queue from cards
                                    where nid == """ + str(nid[0]))
        for queue in nid_queues:
            if queue[0] != -1:
                break
        else:
            sus_nid.append(nid[0])
    self.col.remove_notes(sus_nid)

    self.unloadProfile(self.cleanupAndExit)

AnkiQt.unloadProfileAndExit = unloadProfileAndExit
