
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, extract, case
from app.crud.base import CRUDBase
from app.models.group import Group
from app.models.user import User, UserRole
from app.models.registration import Registration
from app.schemas.group import GroupCreate, GroupUpdate
from datetime import datetime, timedelta

class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def create_with_instructor(
        self, db: Session, *, obj_in: GroupCreate, instructor_id: Optional[int] = None
    ) -> Group:
        obj_in_data = obj_in.dict()
        if instructor_id:
            obj_in_data["instructor_id"] = instructor_id
        db_obj = Group(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_with_details(self, db: Session, id: int) -> Optional[Group]:
        return db.query(Group).options(
            joinedload(Group.instructor),
            joinedload(Group.registrations).joinedload(Registration.visitor)
        ).filter(Group.id == id).first()
    
    def get_multi_with_details(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Group]:
        return db.query(Group).options(
            joinedload(Group.instructor),
            joinedload(Group.registrations).joinedload(Registration.visitor)
        ).offset(skip).limit(limit).all()
    
    def get_upcoming_groups(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Group]:
        now = datetime.now()
        return db.query(Group).options(
            joinedload(Group.instructor)
        ).filter(Group.start_time > now).order_by(Group.start_time).offset(skip).limit(limit).all()
    
    def get_instructor_groups(
        self, db: Session, *, instructor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Group]:
        return db.query(Group).filter(
            Group.instructor_id == instructor_id
        ).order_by(Group.start_time).offset(skip).limit(limit).all()

    def get_visitor_available_groups(self, db: Session, visitor_id: int, gender: str, skip: int = 0, limit: int = 100):
        now = datetime.utcnow()

        # Get the list of groups the visitor is already registered in
        registered_group_ids = db.query(Group.id).join(Group.registrations).filter(
            Registration.visitor_id == visitor_id).all()

        registered_group_ids = [g[0] for g in registered_group_ids]

        # Base query for available groups
        query = db.query(Group).join(
            Registration, Group.id == Registration.group_id, isouter=True
        ).join(
            User, User.id == Registration.visitor_id, isouter=True
        ).filter(
            Group.start_time > now,
            ~Group.id.in_(registered_group_ids) if registered_group_ids else True
        )

        # Aggregation for gender-specific constraints
        if gender == 'male':
            query = query.group_by(Group.id).having(
                func.count(Group.registrations) < Group.capacity,
                func.sum(case(
                    (User.gender == 'male', 1),
                    else_=0
                )) < Group.max_male
            )
        elif gender == 'female':
            query = query.group_by(Group.id).having(
                func.count(Group.registrations) < Group.capacity,
                func.sum(case(
                    (User.gender == 'female', 1),
                    else_=0
                )) < Group.max_female
            )
        else:
            query = query.group_by(Group.id).having(
                func.count(Group.registrations) < Group.capacity
            )

        groups = query.order_by(Group.start_time).offset(skip).limit(limit).all()
        return groups


    
    def update_instructor(
        self, db: Session, *, group_id: int, new_instructor_id: Optional[int]
    ) -> Group:
        group = self.get(db, id=group_id)
        if group:
            group.instructor_id = new_instructor_id
            db.add(group)
            db.commit()
            db.refresh(group)
        return group


group = CRUDGroup(Group)
