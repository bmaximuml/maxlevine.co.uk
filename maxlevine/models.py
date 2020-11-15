from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000), nullable=False)
    priority = db.Column(db.Integer, nullable=False)


class Skill(db.Model):
    name = db.Column(db.String(200), db.ForeignKey('tag.name'), primary_key=True, nullable=False)
    url = db.Column(db.String(500), nullable=True)
    img = db.Column(db.String(200), nullable=True)

    tag = db.relationship("Tag", foreign_keys=name)

    def __repr__(self):
        return f'<Skill {str(self.name)}>'


tags = db.Table(
    'tags',
    db.Column(
        'tag_name',
        db.String(200),
        db.ForeignKey('tag.name'),
        primary_key=True
    ),
    db.Column(
        'project_name',
        db.String(200),
        db.ForeignKey('project.name'),
        primary_key=True
    )
)


class Project(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.Integer, nullable=False)
    tags = db.relationship(
        'Tag',
        secondary=tags,
        lazy='subquery',
        backref=db.backref('projects', lazy=True)
    )


class Tag(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable=False)
    colour = db.Column(db.String(20), nullable=False)

    def __eq__(self, other):
        if other is None:
            return False
        return self.colour == other.colour

    def __ne__(self, other):
        if other is None:
            return True
        return self.colour != other.colour

    def __lt__(self, other):
        if other is None:
            return False
        return self.colour < other.colour

    def __gt__(self, other):
        if other is None:
            return True
        return self.colour > other.colour

    def __le__(self, other):
        if other is None:
            return False
        return self.colour <= other.colour

    def __ge__(self, other):
        if other is None:
            return True
        return self.colour >= other.colour
