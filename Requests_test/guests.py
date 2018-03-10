import requests
import unittest
class GuestTest(unittest.TestCase):
    def testcase1(self):
        r = requests.get("http://127.0.0.1:8000/api/get_event_list", params={"eid":1})
        #print(r.status_code )
        result=r.json()
        self.assertEqual(result["status"],200)
        self.assertEqual(result["message"], "success")

    def testcase2(self):
        pl=dict(eid="22",name="苹果发布会",limit="1000",address="上海",start_time="2018")
        r2 =requests.post("http://127.0.0.1:8000/api/add_event/",data=pl)
        result = r2.json()
        self.assertEqual(result["status"], 10024)
        self.assertIn("发布会时间格式错误",result["message"])




if __name__ =="__main__":
    unittest.main()