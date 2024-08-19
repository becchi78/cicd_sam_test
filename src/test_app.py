import json
import unittest
from src import app


class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler(self):
        # モックのS3イベントデータ
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "my-test-bucket"
                        },
                        "object": {
                            "key": "test-file.txt"
                        }
                    }
                }
            ]
        }

        context = {}  # コンテキストは空のモックで十分です

        # Lambda関数を呼び出して結果を取得
        response = app.lambda_handler(event, context)

        # ステータスコードが200であることを確認
        self.assertEqual(response['statusCode'], 200)

        # レスポンスボディに正しいメッセージが含まれていることを確認
        expected_message = (
            "File test-file.txt processed successfully "
            "from bucket my-test-bucket"
        )
        self.assertEqual(json.loads(response['body']), expected_message)


if __name__ == '__main__':
    unittest.main()
