import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from XrayClassification.cloud_storage.s3_operations import S3Operation
from XrayClassification.entity.artifacts_entity import DataIngestionArtifact
from XrayClassification.entity.config_entity import DataIngestionConfig
from XrayClassification.exception.exception import XRayException
from XrayClassification.logger.logger import logging

class DataIngestion:
    # Hàm khởi tạo
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.s3 = S3Operation()

    # Phương thức này sẽ gọi đến hàm sync_folder_froms3 để lấy data về.
    def get_data_from_s3(self):
        try:
            logging.info("Entered the get_data_from_s3 method of Data...")
            self.s3.sync_folder_from_s3(
                folder=self.data_ingestion_config.data_path,
                bucket_name=self.data_ingestion_config.bucket_name,
                bucket_folder_name=self.data_ingestion_config.s3_data_folder,
            )
            logging.info("Exited the get_data_from_s3 method of Data ingestion")
        
        except Exception as e:
            raise XRayException(e, sys)
        

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the initiate_date_ingestion method of Data ingestion class")
        try:
            self.get_data_from_s3()
            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_data_path,
                test_file_path = self.data_ingestion_config.test_data_path,
            )
            logging.info("Exited the initiate_data_ingestion method of Data ingestion class")
            return data_ingestion_artifact

        except Exception as e:
            raise XRayException(e, sys)