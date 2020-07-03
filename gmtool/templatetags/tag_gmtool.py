from django import template

register = template.Library()


@register.filter
def get_list_item_from_dic(dic, key):
	return dic.get(key, [])


@register.filter
def get_list_item_count(target_list):
	return len(target_list)

