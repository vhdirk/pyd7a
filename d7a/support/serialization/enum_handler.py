import jsonpickle


class EnumHandler(jsonpickle.handlers.BaseHandler):
  def flatten(self, obj, data):
    data = obj.value
    return data