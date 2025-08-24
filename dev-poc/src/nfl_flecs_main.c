#include <flecs.h>
#include <stdio.h>
#include <string.h>

// Taille maximale des champs texte (inclut le '\0')
#define CODE_SIZE  16
#define LINE_SIZE 128

// IMPUT LINE COMPONENT
typedef struct {
    char raw_line[LINE_SIZE]; // Ligne de match en entrée
} GameRawLine;

// GAME COMPONENT 
typedef struct {
    char       season_code[CODE_SIZE];  // ex: "2025"
    char         week_code[CODE_SIZE];  // ex: "WK07"
    char    away_team_code[CODE_SIZE];  // ex: "NYG"
    char    home_team_code[CODE_SIZE];  // ex: "DAL"
    char      stadium_code[CODE_SIZE];  // ex: "MetLife Stadium"
    char     game_day_code[CODE_SIZE];  // ex: "2025-08-18"
    int8_t  away_team_score;
    int8_t  home_team_score;
} Game;

 // CSV OUTPUT LINE COMPONENT
typedef struct {
    char csv_line[LINE_SIZE];
} GameOutCsv;

// INPUT LINE & CSV OUTPUT LINE SEPARATOR
#define SEPARATOR           ','
// Nombre de champs attendus dans la ligne d'entrée
#define EXPECTED_FIELDS      8
// Nombre de séparateurs attendus dans la ligne d'entrée.
#define EXPECTED_SEPARATORS  EXPECTED_FIELDS - 1 
// Pas de SEPARATOR final dans la ligne d'entrée.

int count_separators(const char *line, char sep) {
    int count = 0;
    for (const char *p = line; *p; p++) {
        if (*p == sep) count++;
    }
    return count;
}

#define MY_ENTITY_MONO_COMPONENT_iNDEX 0

// ECS SYSTEM 1: PARSE RAW LINE INTO GAME COMPONENT
void GameStagingSystem(ecs_iter_t *it) {
    GameRawLine *game_raw_lines = ecs_field(it, GameRawLine, MY_ENTITY_MONO_COMPONENT_iNDEX);
    for (int i = 0; i < it->count; i++) {
        const char *input_line = game_raw_lines[i].raw_line;

        int parse_errors = 0 ;
        // Vérification du nombre de séparateurs
        int comma_count = count_separators(input_line, SEPARATOR);
        if (comma_count < EXPECTED_SEPARATORS || comma_count > EXPECTED_SEPARATORS) {
            printf("❌ Ligne %d ignorée (virgules: %d): %s\n", i + 1, comma_count, line);
            parse_errors++;
            continue;
        }

        // Copie locale car strtok modifie la chaîne
        char temp_line[LINE_SIZE];
        memset(temp_line, 0, LINE_SIZE);
        strncpy(temp_line, line, LINE_SIZE);

        
        // Game Component.
        Game g;
        memset(&g, 0, sizeof(Game));

        char* token = strtok(temp_line, SEPARATOR)
        int field = 0 ;

        while(token && field < EXPECTED_FIELDS) {
            switch(field) {
                // DÉFINIT L'ORDRE DES CHAMPS DANS LA LIGNE D'ENTRÉE
                case 0: strncpy(g.season_code   , token, CODE_SIZE); break;
                case 1: strncpy(g.week_code     , token, CODE_SIZE); break;
                case 2: strncpy(g.away_team_code, token, CODE_SIZE); break;
                case 3: g.away_team_score =  atoi(token); break;
                case 4: strncpy(g.home_team_code, token, CODE_SIZE); break;
                case 5: g.home_team_score =  atoi(token); break;
                case 6: strncpy(g.stadium_code  , token, CODE_SIZE); break;
                case 7: strncpy(g.game_day_code , token, CODE_SIZE); break;
            }
            field++
            token = strtok(NULL, SEPARATOR)
        }
        if (field != EXPECTED_FIELDS) {
            printf("❌ Ligne %d ignorée (nb champs lus: %d): %s\n", i+1, field, input_line);
            parse_errors++;
            continue;
        }
//        g.season_code = strtok(game_raw_lines[i].raw_line, ",");
//        g.week_code = strtok(NULL, ",");
//        g.away_team_code = strtok(NULL, ",");
//        g.away_team_score = atoi(strtok(NULL, ","));
//        g.home_team_code = strtok(NULL, ",");
//        g.home_team_score = atoi(strtok(NULL, ","));
//        g.stadium_code = strtok(NULL, ",");
//        g.game_day_code = strtok(NULL, ",");
//        ecs_set(it->world, it->entities[i], Game, g);

        // Ajout dans Flecs ENTITÉ-COMPONENT
        ecs_entity_t e = ecs_new_w_id(it->world, ecs_id(Game));
        ecs_set(ecs, e, ecs_id(Game), { 
            .season_code       = ""
            , .week_code       = ""
            , .away_team_code  = ""
            , .away_team_score = 0
            , .home_team_code  = ""
            , .home_team_score = 0
            , .stadium_code    = ""
            , .game_day_code   = ""
        });

        // Copie manuelle des chaînes 
        // (car Flecs ne copie pas les tableaux char[] automatiquement,
        // Flecs ne copie que les chaines constantes, pas les variables)
        Game *stored = ecs_get_mut_id(it->world, e, ecs_id(Game));
        strncpy(stored->season_code,    g.season_code,    CODE_SIZE);
        strncpy(stored->week_code,      g.week_code,      CODE_SIZE);
        strncpy(stored->away_team_code, g.away_team_code, CODE_SIZE);
        strncpy(stored->home_team_code, g.home_team_code, CODE_SIZE);
        strncpy(stored->stadium_code,   g.stadium_code,   CODE_SIZE);
        strncpy(stored->game_day_code,  g.game_day_code,  CODE_SIZE);
        ecs_modified(ecs, e, ecs_id(Game));
    }
}

// System 2: Add tags or compute fields (placeholder)
void GameTaggingSystem(ecs_iter_t *it) {
    Game *g = ecs_field(it, ecs_id(Game), MY_ENTITY_MONO_COMPONENT_iNDEX);
    for (int i = 0; i < it->count; i++) {
        // add tag for season
        ecs_entity_t season_tag = ecs_entity(it->world, { .name = g[i].season_code });
        ecs_add_id(it->world, it->entities[i], season_tag);
        // add tag for week_code
        ecs_entity_t week_code_tag = ecs_entity(it->world, { .name = g[i].week_code });
        ecs_add_id(it->world, it->entities[i], week_code_tag);
        // add tag for away_team_code
        ecs_entity_t away_team_code_tag = ecs_entity(it->world, { .name = g[i].away_team_code });
        ecs_add_id(it->world, it->entities[i], away_team_code_tag);
        // add tag for away_team_score
        //ecs_entity_t away_team_score_tag = ecs_entity(it->world, { .name = g[i].away_team_score });
        //ecs_add_id(it->world, it->entities[i], away_team_score_tag);
        char score_buf_a[8];
        sprintf(score_buf_a, "%d", g[i].away_team_score);
        ecs_entity_t away_team_score_tag = ecs_entity(it->world, { .name = score_buf_a });
        // add tag for home_team_code
        ecs_entity_t home_team_code_tag = ecs_entity(it->world, { .name = g[i].home_team_code });
        ecs_add_id(it->world, it->entities[i], home_team_code_tag);
        // add tag for home_team_score
        //ecs_entity_t home_team_score_tag = ecs_entity(it->world, { .name = g[i].home_team_score });
        //ecs_add_id(it->world, it->entities[i], home_team_score_tag);
        char score_buf_h[8];
        sprintf(score_buf_h, "%d", g[i].home_team_score);
        ecs_entity_t home_team_score_tag = ecs_entity(it->world, { .name = score_buf_h });
        // add tag for stadium
        ecs_entity_t stadium_tag = ecs_entity(it->world, { .name = g[i].stadium_code });
        ecs_add_id(it->world, it->entities[i], stadium_tag);
        // add tag for game day
        ecs_entity_t game_day_tag = ecs_entity(it->world, { .name = g[i].game_day_code });
        ecs_add_id(it->world, it->entities[i], game_day_tag);
    }
}

// System 3: Generate CSV line
void GameCsvExportSystem(ecs_iter_t *it) {
    Game *g = ecs_field(it, Game, MY_ENTITY_MONO_COMPONENT_iNDEX);
    for (int i = 0; i < it->count; i++) {
        // char *line = malloc(MY_BUFFER_SIZE);
        memset(buffer_line_GameCsvExportSystem, 0, MY_BUFFER_SIZE);
        snprintf(buffer_line_GameCsvExportSystem, MY_BUFFER_SIZE
            , "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"false\",%d,%d,\"false\",\"false\",\"%s\",\"%s\",\"MP4\""
            , g[i].season_code
            , g[i].game_day_code
            , g[i].week_code
            , g[i].away_team_code
            , g[i].home_team_code
            , g[i].stadium_code
            , g[i].home_team_score
            , g[i].away_team_score  // Winner et Looser non traités ici, à voir !
            , g[i].home_team_code   // Haha, on ne sait pas lequel est lequel !
            , g[i].away_team_code   // Haha, on ne sait pas lequel est lequel !
        );
        ecs_set(it->world, it->entities[i], GameOutCsv, { .csv_line = buffer_line_GameCsvExportSystem });
    }
}

void FlecsInit(ecs_world_t *ecs) {
    ECS_COMPONENT(ecs, GameRawLine);
    ECS_COMPONENT(ecs, Game);
    ECS_COMPONENT(ecs, GameOutCsv);

    // ECS_SYSTEM(ecs, GameStagingSystem, EcsOnUpdate, GameRawLine);
    // via macro ecs_system
    // + Nom de l'entité-système ECS
    ecs_system(ecs, {
        .entity = ecs_entity(ecs, {
            .name = "GameStagingSystem",
            .add = ecs_ids( ecs_dependson(EcsOnUpdate) )
        }),
        .query.terms = {
            { ecs_id(GameRawLine) },
        },
        .callback = GameStagingSystem
    });

    ECS_SYSTEM(ecs, GameTaggingSystem, EcsOnUpdate, Game);
    ECS_SYSTEM(ecs, GameCsvExportSystem, EcsOnUpdate, Game);
}
