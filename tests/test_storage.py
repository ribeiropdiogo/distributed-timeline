from storage import local_storage, user_manager, followings_manager
import unittest
import yaml
from datetime import timezone
import datetime


class Test_Update_Storage(unittest.TestCase):

    def test_add_following(self):
        (timeline, following) = local_storage.read_data('database/example.yaml')

        (result_before, fol) = followings_manager.get_following("new_element", following)

        followings_manager.add_following("new_element", following)

        (result_after, fol) = followings_manager.get_following("new_element", following)

        self.assertAlmostEqual(result_after, True)
        self.assertAlmostEqual(result_before, False)
        self.assertNotAlmostEqual(result_before, result_after)

    def test_remove_following(self):
        (timeline, following) = local_storage.read_data('database/example.yaml')

        followings_manager.del_following("node2", following)

        (before, fol) = followings_manager.get_following("node2", following)
        followings_manager.add_following("node2", following)
        (after, fol) = followings_manager.get_following("node2", following)

        self.assertAlmostEqual(before, False)
        self.assertNotAlmostEqual(before, after)

    def test_add_msg_following(self):
        (timeline, following) = local_storage.read_data('database/example.yaml')

        followings_manager.add_following("node10", following)
        (b, fol) = followings_manager.get_following("node10", following)
        tamTimeline1 = len(fol['timeline'])

        timestamp = user_manager.current_time_utc()
        ok2 = followings_manager.add_msg_following(1, "ora viva", timestamp, "node10", following)
        (b, fol) = followings_manager.get_following("node10", following)
        tamTimeline2 = len(fol['timeline'])

        self.assertAlmostEqual(b, True)
        self.assertAlmostEqual(ok2, True)
        self.assertAlmostEqual(tamTimeline1, 0)
        self.assertAlmostEqual(tamTimeline2, 1)


    def test_rm_messages_following(self):
        (timeline, following) = local_storage.read_data('database/example.yaml')

        followings_manager.add_following("node10", following)
        timestamp = user_manager.current_time_utc()
        followings_manager.add_msg_following(1, "ora viva 1", timestamp, "node10", following)
        followings_manager.add_msg_following(2, "ora viva 2", timestamp, "node10", following)
        followings_manager.add_msg_following(3, "ora viva 3", timestamp, "node10", following)
        followings_manager.add_msg_following(4, "ora viva 4", timestamp, "node10", following)
        followings_manager.add_msg_following(5, "ora viva 5", timestamp, "node10", following)
        followings_manager.add_msg_following(6, "ora viva 6", timestamp, "node10", following)
        followings_manager.add_msg_following(7, "ora viva 7", timestamp, "node10", following)
        followings_manager.add_msg_following(8, "ora viva 8", timestamp, "node10", following)
        followings_manager.add_msg_following(9, "ora viva 9", timestamp, "node10", following)
        followings_manager.add_msg_following(10, "ora viva 10", timestamp, "node10", following)
        followings_manager.add_msg_following(11, "ora viva 11", timestamp, "node10", following)
        followings_manager.add_msg_following(12, "ora viva 12", timestamp, "node10", following)
        followings_manager.add_msg_following(13, "ora viva 13", timestamp, "node10", following)

        followings_manager.add_msg_following(1, "ora viva 1", timestamp, "node2", following)

        n_msgs_del = followings_manager.del_msg_following("node10", following)
        n_msgs_del2 = followings_manager.del_msg_following("node2", following)

        self.assertAlmostEqual(n_msgs_del, 3)
        self.assertAlmostEqual(n_msgs_del2, 0)

    def test_my_timeline(self):
        (timeline, following) = local_storage.read_data('database/example.yaml')

        user_manager.add_msg_timeline("Adicionei uma nova mensagem na minha timeline", timeline)

        tam = len(timeline)

        self.assertAlmostEqual(tam, 4)

        n = user_manager.del_timeline_event(4, timeline)

        id_msg = len(timeline)

        self.assertAlmostEqual(id_msg, 3)