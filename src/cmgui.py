def left_lung_command(subject):
    return f"""
### 
### SCRIPT TO CREAT GROUPS AND SAMPLE POINTS FOR EACH GROUP.
###
set dir "{subject}";
#
#
#
# READ MESH:
gfx read node surface "Left_fitted.exnode";
gfx read elem surface "Left_fitted.exelem";
#
#
#
# CREATE GROUPS:
# base
gfx cre egroup "base";
gfx mod egroup "base" add elements 101..104,106..109;
gfx mod egroup "base" add lines 1,3,5,7,10..11,13..14,16..19,21..24,26,30;
# medial
gfx cre egroup "medial";
gfx mod egroup "medial" add elements 69..73,80..83,89..91,97..99;
gfx mod egroup "medial" add lines 2..3,15..16,25..27,29..31,33..34,43..44,47..50,52,54..55,61..62,65..67,69..70,75..80;
# lateral
gfx cre egroup "lateral";
gfx mod egroup "lateral" add elements 63..67,75..78,85..87,93..94,96;
gfx mod egroup "lateral" add lines 1..2,4..6,9..10,12..13,15,32,34..38,41..42,44,53,55..59,62,68,70..74,76,80
# anterior border
gfx cre egroup "anterior";
gfx mod egroup "anterior" add lines 2,34,55,70
#
#
#
# WANT HIGH RES POINT SAMPLING:
gfx define tessellation default minimum_divisions "1" refinement_factors "1" circle_divisions 3;
gfx def field surface_density1 const 0.15;
gfx def field line_density1 const 0.65;
#
#
#
# CREATE REGION TO ADD SAMPLED POINTS:
gfx create region sample;
gfx define field sample/coordinates finite_element num 3 coordinate component_names x y z;
#
#
#
# START SAMPLING:
# base:
gfx create ngroup "base" region sample;
gfx modify g_element "/" general clear;
gfx modify g_element "/" surfaces domain_mesh2d subgroup "base" coordinate coordinates face all tessellation default LOCAL select_on invisible material default selected_material default_selected render_shaded;
gfx modify g_element "/" points domain_mesh2d subgroup "base.mesh2d" coordinate coordinates face all tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default cell_poisson density surface_density1 select_on material default selected_material default_selected render_shaded;
gfx convert graphics coordinate coordinates render_nodes region "sample/base"
gfx modify g_element /sample/ general clear;
gfx modify g_element /sample/ points domain_nodes subgroup "base" coordinate coordinates tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default select_on material green selected_material default_selected render_shaded;
# medial:
gfx create ngroup "medial" region sample;
gfx modify g_element "/" general clear;
gfx modify g_element "/" surfaces domain_mesh2d subgroup "medial" coordinate coordinates face all tessellation default LOCAL select_on invisible material default selected_material default_selected render_shaded;
gfx modify g_element "/" points domain_mesh2d subgroup "medial.mesh2d" coordinate coordinates face all tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default cell_poisson density surface_density1 select_on material default selected_material default_selected render_shaded;
gfx convert graphics coordinate coordinates render_nodes region "sample/medial"
gfx modify g_element /sample/ general clear;
gfx modify g_element /sample/ points domain_nodes subgroup "medial" coordinate coordinates tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default select_on material green selected_material default_selected render_shaded;
# lateral:
gfx create ngroup "lateral" region sample;
gfx modify g_element "/" general clear;
gfx modify g_element "/" surfaces domain_mesh2d subgroup "lateral" coordinate coordinates face all tessellation default LOCAL select_on invisible material default selected_material default_selected render_shaded;
gfx modify g_element "/" points domain_mesh2d subgroup "lateral.mesh2d" coordinate coordinates face all tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default cell_poisson density surface_density1 select_on material default selected_material default_selected render_shaded;
gfx convert graphics coordinate coordinates render_nodes region "sample/lateral"
gfx modify g_element /sample/ general clear;
gfx modify g_element /sample/ points domain_nodes subgroup "lateral" coordinate coordinates tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default select_on material green selected_material default_selected render_shaded;
# anterior border:
gfx create ngroup "anterior" region sample;
gfx modify g_element "/" general clear;
gfx modify g_element "/" lines domain_mesh1d subgroup anterior coordinate coordinates face all tessellation default LOCAL line line_base_size 2 select_on material default selected_material default_selected render_shaded;
gfx modify g_element "/" points domain_mesh1d subgroup "anterior.mesh1d" coordinate coordinates face all tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default cell_poisson density line_density1 select_on material default selected_material default_selected render_shaded;
gfx convert graphics coordinate coordinates render_nodes region "sample/anterior"
gfx modify g_element /sample/ general clear;
gfx modify g_element /sample/ points domain_nodes subgroup "lateral" coordinate coordinates tessellation default_points LOCAL glyph point size "1*1*1" offset 0,0,0 font default select_on material green selected_material default_selected render_shaded;
#
#
#
# EXPORT THE SAMPLED NODES
gfx write node group "/sample" field coordinates "Left_points.exnode";
quit;
"""
