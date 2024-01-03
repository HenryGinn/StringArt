from art import Art

my_art = Art("BirdImage", "BirdImage.png")
my_art.setup_position(force=False)
print(my_art.position_setup)

my_art.display_obj.root.mainloop()
