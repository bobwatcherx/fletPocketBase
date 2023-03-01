from flet import *
from pocketbase import PocketBase
client = PocketBase("http://127.0.0.1:8090")


def main(page:Page):
	page.scroll = "auto"
	username = TextField(label="username")
	email = TextField(label="email")
	password = TextField(label="password")

	editid = Text()

	listalluserresult = Column()


	def addnewuser(e):
		try:
			record = client.collection("users").create(body_params={
				"username":username.value,
				"name":username.value,
				"email":email.value,
				"password":password.value,
				"passwordConfirm":password.value	
				})
			print(record)
			# CLEAR ALL DATA AND CALL FUNCTION AGAIN

			listalluserresult.controls.clear()
			get_all_user()
			page.snack_bar = SnackBar(
				Text("success add user",size=30),
				bgcolor="blue"
				)
			page.snack_bar.open = True
			page.update()
		except Exception as e:
			print(e)
			print("ERROR CHECK !!!")

	def deleteuser(e):
		youdeleteid = e.control.data
		admin_data = client.admins.auth_with_password("bobwatcherx@gmail.com","admin12345")
		alluser = client.collection("users").delete(youdeleteid)

		# CLEAR AND CALL AGAIN
		listalluserresult.controls.clear()
		get_all_user()

		# AND SHOW SnackBar
		page.snack_bar = SnackBar(
			Text("Succes deleted",size=30),
			bgcolor="red"
			)
		page.snack_bar.open = True
		page.update()
		

	def savedatanow(e):
		admin_data = client.admins.auth_with_password("bobwatcherx@gmail.com","admin12345")
		alluser = client.collection("users").update(editid.value,{
			# YOU FIELD FOR CHANGE LIKE PASSWORD
			# USERNAME EMAIL OR AVATAR IMAGE
			# I CHANGE ONLY USERNAME AND EMAIL
			# YOU WHATEVER
			"username":username.value,
			"email":email.value
			})
		listalluserresult.controls.clear()
		get_all_user()
		dialog.open = False
		page.snack_bar = SnackBar(
			Text("success add user",size=30),
				bgcolor="blue"
				)
		page.snack_bar.open = True
		page.update()



	dialog = AlertDialog(
		title=Text("Edit data"),
		content=Column([
			username,
			email
			]),
		actions=[
			TextButton("save data",
				on_click=savedatanow
				)
		]
		)

	def edituser(e):
		editid.value = e.control.data.id
		username.value = e.control.data.username
		email.value = e.control.data.email
		page.dialog = dialog 
		dialog.open = True
		page.update()
		





	# GET ALL USER FROM COLLECTION POCKETBASE
	def get_all_user():
		# YOU ADMIN ACCOUT IN POCKETBASE

		admin_data = client.admins.auth_with_password("bobwatcherx@gmail.com","admin12345")
		alluser = client.collection("users").get_full_list()
		for x in alluser:
			listalluserresult.controls.append(
				Container(
					bgcolor="blue200",
					padding=10,
					content=Column([
						Row([
						Text(x.username,size=25,weight="bold"),
						Text(x.created)
							],alignment="spaceBetween"),
						Text(f"email : {x.email}"),
						Text(f"verified : {x.verified}"),

					# AND NOW CREATE BUTTON EDIT AND DELETE
					IconButton("delete",
						bgcolor="red",icon_color="white",
						data=x.id,
						on_click=deleteuser
						),
					IconButton("edit",
						bgcolor="blue",icon_color="white",
						data=x,
						on_click=edituser
						),

						],alignment="spaceBetween")

					)

				)

		page.update()

	# AND CALL FUNCTION WHEN FLET APP IS FIRST OPEN
	# THE ALL DATA WILL APPEND TO WIDGET COLUMN
	# FROM COLLECTION POCKETBASE

	get_all_user()


	page.add(
	Column([
		Text("Pocketbase user crud",size=30),
		username,
		email,
		password,
		ElevatedButton("Add new user",
			bgcolor="blue",color="white",
			on_click=addnewuser
			),
		listalluserresult

		])

		)
flet.app(target=main)


