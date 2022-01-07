# -*- coding: utf-8 -*-
import os


class ItemNameConverter:    

    def __init__(self):
        self._item_name_data = [];
        
        with open('assets/item_names.csv', 'r', encoding='utf-8') as data:
            lines = data.readlines();    
            
        for line in lines:
            temp = line.rstrip().split(',');
            if len(temp) < 2:
                continue;
            temp[ 0 ] = temp[ 0 ].lower();
            temp[ 0 ] = temp[ 0 ].replace( "'s", "" );
            temp[ 0 ] = temp[ 0 ].replace( "'a", "a" );
            temp[ 0 ] = temp[ 0 ].replace( "'", "" );
            temp[ 0 ] = temp[ 0 ].replace( " ", "_");
            self._item_name_data.append( [ temp[0], temp[1]  ] )
            # print( [ temp[0], temp[1]  ] );
            
    def get_item_name(self, item_name: str) -> str:        
        temp_name = item_name;
        postfix_name = ''
        
        if "white_" in temp_name:
            temp_name = temp_name.replace( "white_", "" );
            temp_name = temp_name.replace( "weapon_", "" );
            temp_name = temp_name.replace( "armor_", "" );
            temp_name = temp_name.replace( "helm_", "" );
            temp_name = temp_name.replace( "shield_", "" );
            temp_name = temp_name.replace( "superior_", "" );
            postfix_name = ' (노멀)'
            
        if "magic_" in temp_name:
            temp_name = temp_name.replace( "magic_", "" );
            postfix_name = ' (매직)'
            
        if "rare_" in temp_name:
            temp_name = temp_name.replace( "rare_", "" );
            postfix_name = ' (레어)'
            
        if "gray_" in temp_name:
            temp_name = temp_name.replace( "gray_", "" );
            temp_name = temp_name.replace( "weapon_", "" );
            temp_name = temp_name.replace( "armor_", "" );
            temp_name = temp_name.replace( "helm_", "" );
            temp_name = temp_name.replace( "shield_", "" );
            temp_name = temp_name.replace( "superior_", "" );
            postfix_name = ' (회색)'
            
        if "uniq_" in temp_name:
            temp_name = temp_name.replace( "uniq_armor_", "" );
            temp_name = temp_name.replace( "uniq_belt_", "" );
            temp_name = temp_name.replace( "uniq_boots_", "" );
            temp_name = temp_name.replace( "uniq_gloves_", "" );
            temp_name = temp_name.replace( "uniq_helm_", "" );
            temp_name = temp_name.replace( "uniq_offhand_", "" );
            temp_name = temp_name.replace( "uniq_weapon_", "" );
            temp_name = temp_name.replace( "uniq_misc_", "" );
            temp_name = temp_name.replace( "uniq_", "" );            
            postfix_name = ' (유니크)'
            
        if "set_" in temp_name:
            temp_name = temp_name.replace( "set_misc_", "" );
            temp_name = temp_name.replace( "set_", "" );
            postfix_name = ' (세트)'
        
        N = len( self._item_name_data )
        for index in range(N):
            if temp_name in self._item_name_data[ index ][ 0 ]:
                return self._item_name_data[ index ][ 1 ] + postfix_name;
                
        return item_name
