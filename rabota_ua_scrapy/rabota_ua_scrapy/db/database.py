import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Base, Job
from ..config import POSTGRESQL_CONNECTION_URL


class Database:

    def __init__(self):
        self.engine = create_engine(POSTGRESQL_CONNECTION_URL)
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)
        self.logger = logging.getLogger('DATABASE')
        logging.basicConfig()
        self.logger.setLevel('INFO')

    def add_job(
            self,
            job: Job,
    ) -> None:
        job_entry_from_db = self.session.query(Job) \
            .filter_by(url=job.url).one_or_none()
        self._merge_jobs(
            current=job,
            base=job_entry_from_db,
        )
        self.commit()

    def _merge_jobs(
            self,
            current: Job,
            base: Job,
    ) -> None:
        if base:
            self.session.merge(current)
            self.logger.info(f'Updated job with url: [{current.url}]')
        else:
            self.session.add(current)
            self.logger.info(f'Saved job with url: [{current.url}]')

    def commit(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as e:
            self.logger.error(e)
            self.session.rollback()
        except Exception as e:
            self.session.rollback()
            raise e
