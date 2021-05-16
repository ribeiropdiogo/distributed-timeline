from storage import local_storage, update_storage
import unittest
import yaml

class Test_Update_Storage(unittest.TestCase):

    def test_add_following(self):
        (identity, username, timeline, following) = local_storage.read_data('database/content.yaml')

        (result_before, fol) = update_storage.get_one_following("new_element", following)
        
        update_storage.add_following("new_element", "new_element_username", "0.0.0.0", 12347, following)
        
        (result_after, fol) = update_storage.get_one_following("new_element", following)
        
        self.assertAlmostEqual(result_after, True)
        self.assertAlmostEqual(result_before, False)
        self.assertNotAlmostEqual(result_before, result_after)

        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/","fileTestAddFollowing")


    def test_remove_following(self):
        (identity, username, timeline, following) = local_storage.read_data('database/content.yaml')

        update_storage.del_following("node2", following)

        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/", "fileTestRemove")

        (before, fol) = update_storage.get_one_following("node2", following)

        update_storage.add_following("node2", "nobody@mail.com", "0.0.0.0", 10002, following)

        (after, fol) = update_storage.get_one_following("node2", following)

        self.assertAlmostEqual(before, False)
        self.assertNotAlmostEqual(before, after)

    def test_add_msg_following(self):
        (identity, username, timeline, following) = local_storage.read_data('database/content.yaml')

        update_storage.add_following("node10", "someNode@mail.com", "0.0.0.0", 11112, following)

        update_storage.add_msg_following_timeline(1, "ora viva", "node10", following)

        (b, fol) = update_storage.get_one_following("node10", following)

        #Messages without order
        update_storage.add_msg_following_timeline(5, "ora viva fora de ordem", "node10", following)

        n_msg = len(fol['timeline'])

        n_track = fol['track_timeline']

        self.assertAlmostEqual(n_msg, 1)
        self.assertAlmostEqual(n_track, 1)

        #Messages in order
        update_storage.add_msg_following_timeline(2, "ora viva outra vez", "node10", following)
        n_msg = len(fol['timeline'])
        n_track = fol['track_timeline']

        self.assertAlmostEqual(n_msg, 2)
        self.assertAlmostEqual(n_track, 2)
        self.assertAlmostEqual(n_msg, n_track)


        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/", "addMsgFollowing")
    
    def test_rm_messages_following(self):
        (identity, username, timeline, following) = local_storage.read_data('database/content.yaml')

        update_storage.add_following("node10", "someNode@mail.com", "0.0.0.0", 11112, following)
        update_storage.add_msg_following_timeline(1, "ora viva 1", "node10", following)
        update_storage.add_msg_following_timeline(2, "ora viva 2", "node10", following)
        update_storage.add_msg_following_timeline(3, "ora viva 3", "node10", following)
        update_storage.add_msg_following_timeline(4, "ora viva 4", "node10", following)

        n_msgs_del = update_storage.del_msg_following_timeline(2,"node10", following)

        n_msgs_del2 = update_storage.del_msg_following_timeline(2,"node2", following)

        self.assertAlmostEqual(n_msgs_del, 2)
        self.assertAlmostEqual(n_msgs_del2, 0)

        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/", "rmMsgsFollowing")


    def test_my_timeline(self):
        (identity, username, timeline, following) = local_storage.read_data('database/content.yaml')

        update_storage.add_msg_my_timeline("Adicionei uma nova mensagem na minha timeline", timeline)

        tam = len(timeline)

        self.assertAlmostEqual(tam, 4)

        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/", "addMsgTimeline")

        n = update_storage.del_timeline_event(4, timeline)

        id_msg = len(timeline)

        local_storage.save_data_in_path(identity, username, timeline, following, "filesTest/", "rmMsgTimeline")

        self.assertAlmostEqual(id_msg, 3)
