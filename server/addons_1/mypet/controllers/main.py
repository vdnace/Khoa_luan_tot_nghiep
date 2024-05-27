import odoo
import logging
import json

_logger = logging.getLogger(__name__)

class MyPetAPI(odoo.http.Controller):
    @odoo.http.route('/foo', auth='public')
    def foo_handler(self):
        return "Welcome to 'foo' API!"
    
    @odoo.http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })
    
    @odoo.http.route(['/pet/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def pet_handler(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            _logger.info("Querying database for pet with ID %s", id)
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if rec:
                    _logger.info("Found pet: %s", rec.name)
                    response = {
                        "status": "ok",
                        "content": {
                            "name": rec.name,
                            "nickname": rec.nickname,
                            "description": rec.description,
                            "age": rec.age,
                            "weight": rec.weight,
                            "dob": rec.dob.strftime('%d/%m/%Y'),
                            "gender": rec.gender,
                        }
                    }
                else:
                    _logger.warning("Pet with ID %s not found", id)
                    response = {
                        "status": "error",
                        "content": "not found"
                    }
        except Exception as e:
            _logger.error("Error while querying database: %s", str(e))
            response = {
                "status": "error",
                "content": "error"
            }
        return json.dumps(response)