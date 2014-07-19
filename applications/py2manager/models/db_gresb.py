# db.define_table('electric_bb',
# 	Field('company_name','reference company',notnull=True),
# 	Field('building_name','reference building',notnull=True),
# 	Field('reporting_year', 'integer', notnull=True),
# 	Field('usage','float'),
# 	Field('usage_units','reference energy_units',notnull=True),
# 	Field('cost','float'),
# 	Field('cost_units', 'reference cost_units'),
# 	format = '%(company_name)s'
# 	)


# db.define_table('building',
# 	Field('name', notull=True, unique=True),
# 	Field('area', 'float', notnull=True)
# 	)

# db.define_table('energy_units',
# 	Field('unit','text',notnull=True, unique=True),
# 	Field('to_btu','float',notnull=True)
# 	)

# db.define_table('cost_units',
# 	Field('name', 'text',notull=True,unique=True),
# 	Field('to_USD','float',notull=True)
# 	)
