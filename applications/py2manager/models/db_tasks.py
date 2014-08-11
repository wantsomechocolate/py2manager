db.define_table('company',
	Field('company_name'),
	Field('email'),
	Field('phone'),
	Field('url'),
	)

#db.auth_user.company.requires=IS_IN_DB(db,'company.company_name', '%(company_name)s')
#db.auth_user.company.writable=False
#db.auth_user.company.default="None"

db.company.email.requires=IS_EMAIL()
db.company.url.requires=IS_EMPTY_OR(IS_URL())

db.define_table('project',
	Field('name', notnull=True),
	Field('employee_name', db.auth_user, default=auth.user_id),
	Field('company_name', 'reference company', notnull=True),
	Field('description', 'text', notnull=True),
	Field('start_date', 'date', notnull=True),
	Field('due_date','date', notnull=True),
	Field('completed','boolean', notnull=True),
	#Field('modified_on'),
	#Field('modified_by'),
	format = '%(company_name)s'
	)

db.project.employee_name.readable = db.project.employee_name.writeable=False

#db.project.employee_name.readable = db.project.employee_name.writable = False
#db.project.company_name.readable = False
#db.project.company_name.writable = False


# db.project.start_date.requires = IS_DATE(format=T('%m-%d-%Y'),
# 	error_message='Must be MM-DD-YYYY!')

# db.project.due_date.requires =IS_DATE(format=T('%m-%d-%Y'),
# 	error_message='Must be MM-DD-YYYY!')

db.define_table('note',
	Field('post_id', 'reference project', writable=False),
	Field('post', 'text', notnull=True),
	Field('created_on', 'datetime', default=request.now, writable=False),
	Field('created_by', db.auth_user, default = auth.user_id)
	)

db.note.post_id.readable = db.note.post_id.writable=False
db.note.created_on.readable = db.note.created_on.writable=False
db.note.created_on.requires = IS_DATE(format=T('%m-%d-%Y'),
	error_message='Must be MM-DD-YYYY!')
db.note.created_by.readable = db.note.created_by.writable=False


db.define_table('cost_units',
	Field('name', notnull=True, unique=True),
	Field('to_USD', notnull=True),
	format = '%(name)s'
	)

db.define_table('energy_units',
	Field('unit',notnull=True, unique=True),
	Field('to_btu','float',notnull=True),
	format = '%(unit)s'
	)

db.define_table('area_units',
	Field('area_unit',notnull=True, unique = True),
	Field('to_SF','float', notnull=True),
	format = '%(area_unit)s'
	)

## - Building Information
db.define_table('buildings',
	Field('company_name'),
	Field('building_name', notnull=True, unique=True),
	Field('building_area', 'float', notnull=True),
	Field('purchase_date', 'date'),
	Field('sell_date','date'),
	format = '%(building_name)s'
	)

#db.buildings.company_name.readable = False
#db.buildings.id.readable=False
#db.buildings.company_name.writable = False
#db.project.company_name.default="None"

db.buildings.purchase_date.requires=IS_DATE(format=T('%m-%d-%Y'),
	error_message='Must by MM-DD-YYYY!')
db.buildings.sell_date.requires=IS_EMPTY_OR(IS_DATE(format=T('%m-%d-%Y'),
	error_message='Must by MM-DD-YYYY!'))

##-Electric Table Fields

db.define_table('electric_test',
	Field('company_name', unique=True, notnull=True),

	Field('building_name'),
	
	Field('reporting_year', 'integer', notnull=True),

	Field('total_base_building_usage'),
	Field('total_base_building_usage_units'),
	Field('total_base_building_cost'),
	Field('total_base_building_cost_units'),
	Field('total_base_building_area'),

	Field('total_tenant_submeter_usage'),
	Field('total_tenant_submeter_usage_units','reference energy_units'),
	Field('total_tenant_submeter_cost','float'),
	Field('total_tenant_submeter_cost_units', 'reference cost_units'),
	Field('total_tenant_submeter_area'),

	Field('total_tenant_direct_usage'),
	Field('total_tenant_direct_usage_units','reference energy_units'),
	Field('total_tenant_direct_cost','float'),
	Field('total_tenant_direct_cost_units', 'reference cost_units'),
	Field('total_tenant_direct_area'),
	#format = ['%(building_name)s','%(company_name)s']
	)

##-- Electric Table requirements
db.electric_test.total_base_building_usage.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_base_building_usage_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'energy_units.id', '%(unit)s'))
db.electric_test.total_base_building_cost.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_base_building_cost_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'cost_units.id', '%(name)s'))

db.electric_test.total_tenant_submeter_usage.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_tenant_submeter_usage_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'energy_units.id', '%(unit)s'))
db.electric_test.total_tenant_submeter_cost.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_tenant_submeter_cost_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'cost_units.id', '%(name)s'))

db.electric_test.total_tenant_direct_usage.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_tenant_direct_usage_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'energy_units.id','%(unit)s'))
db.electric_test.total_tenant_direct_cost.requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, 1e100))
db.electric_test.total_tenant_direct_cost_units.requires=IS_EMPTY_OR(IS_IN_DB(db, 'cost_units.id', '%(name)s'))


#db.electric_test.total_tenant_submeter_usage.requires=(db.electric_test.total_base_building_usage>db.electric_test.total_tenant_submeter_usage)
#db.electric_test.company_name.writable = False
#db.electric_test.id.readable=False
#db.electric_test.company_name.default=auth.user.company
#db.electric_test.building_name.requires=IS_IN_DB(db(db.electric_test.building_name==auth.user.company),'electric_test.building_name')
