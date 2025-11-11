"""
Freelancer Schema (Validation & Serialization)
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class SkillSchema(Schema):
    """스킬 스키마"""
    id = fields.String(required=True)
    name = fields.String(required=True)
    level = fields.String(missing='intermediate', validate=validate.OneOf(['beginner', 'intermediate', 'advanced', 'expert']))
    category = fields.String(required=True)
    endorsements = fields.Integer(missing=0)
    certified = fields.Boolean(missing=False)

    class Meta:
        fields = ('id', 'name', 'level', 'category', 'endorsements', 'certified')


class FreelancerSchema(Schema):
    """프리랜서 응답 스키마"""
    id = fields.String()
    name = fields.String()
    email = fields.Email()
    phone = fields.String()
    experience = fields.Integer()
    hourlyRate = fields.Integer()
    avatar = fields.String(allow_none=True)
    bio = fields.String(allow_none=True)
    availability = fields.String()
    rating = fields.Float()
    reviewCount = fields.Integer()
    portfolio = fields.List(fields.String())
    skills = fields.List(fields.Nested(SkillSchema))
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()

    class Meta:
        fields = (
            'id', 'name', 'email', 'phone', 'experience', 'hourlyRate',
            'avatar', 'bio', 'availability', 'rating', 'reviewCount',
            'portfolio', 'skills', 'createdAt', 'updatedAt'
        )


class FreelancerCreateSchema(Schema):
    """프리랜서 생성 스키마"""
    name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Regexp(r'^\d{3}-\d{4}-\d{4}$'))
    experience = fields.Integer(required=True, validate=validate.Range(min=0))
    hourlyRate = fields.Integer(required=True, validate=validate.Range(min=0))
    availability = fields.String(required=True, validate=validate.OneOf(['available', 'busy', 'unavailable']))
    avatar = fields.String(allow_none=True)
    bio = fields.String(allow_none=True)
    skillIds = fields.List(fields.String(), required=True, validate=validate.Length(min=1))

    class Meta:
        fields = ('name', 'email', 'phone', 'experience', 'hourlyRate', 'avatar', 'bio', 'availability', 'skillIds')

    @validates('skillIds')
    def validate_skills(self, value):
        """최소 1개 이상의 스킬 필요"""
        if not value or len(value) == 0:
            raise ValidationError('최소 1개 이상의 스킬을 선택해주세요')


class FreelancerUpdateSchema(Schema):
    """프리랜서 수정 스키마"""
    name = fields.String(validate=validate.Length(min=2))
    email = fields.Email()
    phone = fields.String(validate=validate.Regexp(r'^\d{3}-\d{4}-\d{4}$'))
    experience = fields.Integer(validate=validate.Range(min=0))
    hourlyRate = fields.Integer(validate=validate.Range(min=0))
    availability = fields.String(validate=validate.OneOf(['available', 'busy', 'unavailable']))
    avatar = fields.String(allow_none=True)
    bio = fields.String(allow_none=True)
    skillIds = fields.List(fields.String())

    class Meta:
        fields = ('name', 'email', 'phone', 'experience', 'hourlyRate', 'avatar', 'bio', 'availability', 'skillIds')
