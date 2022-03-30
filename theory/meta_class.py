import copy
from functools import lru_cache
from functools import wraps
import json

def make_hash(p_item):

  """
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """

  if isinstance(p_item, (set, tuple, list)):

    return tuple([make_hash(e) for e in p_item])    

  elif not isinstance(p_item, dict):

    return hash(p_item)

  #new_item = copy.deepcopy(p_item)
  new_item = p_item

  for k, v in new_item.items():
    new_item[k] = make_hash(v)

  return hash(tuple(frozenset(sorted(new_item.items()))))

def hashable_lru(func):
    cache = lru_cache(maxsize=1024)

    def deserialise(value):
        try:
            return json.loads(value)
            
        except Exception:
            return value

    def func_with_serialized_params(*args, **kwargs):
        _args = tuple([deserialise(arg) for arg in args])
        _kwargs = {k: deserialise(v) for k, v in kwargs.items()}
        return func(*_args, **_kwargs)

    cached_function = cache(func_with_serialized_params)

    @wraps(func)
    def lru_decorator(*args, **kwargs):
        _args = tuple([json.dumps(arg, sort_keys=True, default=lambda o: o.toJson()) if type(arg) in (list, dict) else arg for arg in args])
        _kwargs = {k: json.dumps(v, sort_keys=True, default=lambda o: o.toJson()) if type(v) in (list, dict) else v for k, v in kwargs.items()}
        return cached_function(*_args, **_kwargs)

    lru_decorator.cache_info = cached_function.cache_info
    lru_decorator.cache_clear = cached_function.cache_clear
    return lru_decorator

def to_json(p_object, p_references):
  new_dict = {}

  for key, value in p_object.get_attributes().items():
    item_id = id(value)
    
    if item_id in p_references:
      new_dict[key] = item_id

    else: 
      p_references[item_id] = p_object
      new_dict[key] = json.dumps(value, default = lambda x: to_json(x, p_references))

  return new_dict