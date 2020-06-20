from app import db
from app.src.models import User, Art

# db.drop_all()
# db.create_all()

user = User.query.filter_by(username="test").first()

# art = Art(title="Test", description="Test description", img_id="image id", author=user)
art2 = Art(title="Test 1", description="Test 2 description", img_id="image 2 id", author=user)
art3 = Art(title="Test 3", description="Test 3 description", img_id=43729847329847, img_extenstion="jpg",author=user)

db.session.add(art2)
db.session.add(art3)
db.session.commit()
