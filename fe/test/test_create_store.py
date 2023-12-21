import pytest

from fe.access.new_seller import register_new_seller
import uuid


class TestCreateStore:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_create_store_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_create_store_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        yield

    def test_ok(self):
        self.seller = register_new_seller(self.user_id, self.password)
        seller = self.seller.seller_id
        code = self.seller.create_store1(seller,self.store_id)
        assert code == 200

    def test_error_exist_store_id(self):
        self.seller = register_new_seller(self.user_id, self.password)
        seller = self.seller.seller_id
        code = self.seller.create_store1(seller,self.store_id)
        assert code == 200

        code = self.seller.create_store1(seller,self.store_id)
        assert code != 200

    def test_error_exist_user_id(self):
        self.seller = register_new_seller(self.user_id, self.password)
        seller=self.seller.seller_id
        code = self.seller.create_store1(seller+"_x",self.store_id)
        assert code != 200







