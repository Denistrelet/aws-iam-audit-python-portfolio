from aws_iam_audit.audit import list_active_accounts


class FakePaginator:
    def paginate(self):
        return [
            {
                "Accounts": [
                    {"Id": "111", "Name": "dev", "Status": "ACTIVE"},
                    {"Id": "222", "Name": "suspended", "Status": "SUSPENDED"},
                ]
            }
        ]


class FakeOrgClient:
    def get_paginator(self, name):
        assert name == "list_accounts"
        return FakePaginator()


def test_list_active_accounts_filters_non_active():
    accounts = list_active_accounts(FakeOrgClient())
    assert len(accounts) == 1
    assert accounts[0].id == "111"
    assert accounts[0].name == "dev"
