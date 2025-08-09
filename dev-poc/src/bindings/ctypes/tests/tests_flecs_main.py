from flecs import *

if __name__ == "__main__":
    # Monde
    world = binded_ecs_init()
    # Entité
    entity = binded_ecs_new(world)

    # Composant HTML
    # 1 REGISTER
    html_component_id = register_html_component(world)
    # 2 SET
    # Entité métier à composant HTML avec contenu HTML
    set_html_component(world, entity, html_component_id, "<html>Test</html>")

    # Attente
    time.sleep(5)

    # 3. RETRIEVE
    # Récupération du composant
    retrieved = get_component_data(world, entity, html_component_id, CHTMLComponent)
    if retrieved:
        html_str = bytes(retrieved.html).decode("utf-8").rstrip("\x00")
        print("Contenu HTML extrait du composant de l'entité :", html_str)

    # Terminer le monde
    binded_ecs_fini(world)
