#include "avr/io.h"
#include "util/delay.h"
#include "lcd.h"
#include <avr/interrupt.h>
#include <stdbool.h>
#define MAX_STR 50
#define BAUD 9600
#include "uart.h"
#include "mat_kbrd.h"

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
int main(void)
{
        serial_begin();
        i2c_init();
        lcd_init();
	kbrd_init();	
   
	char tipoDesecho = "";
	char cantidadDesechos[]="";
	char key;
   	char key2;
        char str[20];
	int size = 0;

	lcd_msg("   BIENVENIDO");
	lcd_cursor(1,0);
       _delay_ms(500);
	lcd_msg("   AL PROGRAMA   ");
	_delay_ms(500);
	lcd_clrscr();
	
    while(1)
    {
                lcd_init();	  	
                lcd_msg(" RESIDUO (I/NI)");
		lcd_cursor(1,0);
		lcd_msg("  I:ON    NI:=");
		do{
			key=kbrd_read();
		        if(key=="="){
			   tipoDesecho="Residuo no Industrial";
			   }
			if(key=="."){
			   tipoDesecho="Residuo Industrial";
			   }   
		}while (!(key!='=') ^ (key!='.'));
		lcd_init();
		lcd_msg("CANTIDAD BASURA:");
		do{
		        lcd_cursor(1,0);
		        key2=kbrd_read();
		        if(key2!=0){
			   cantidadDesechos[size]=key2;
			   lcd_cursor(1,0);
			   lcd_msg("    	");
			   str[0]=cantidadDesechos;
			   lcd_msg(str);
			   lcd_msg("KG");
			   size++;
			   printf(str);
			}
		}while(key2!='=');
		size = 0;
		lcd_init();
                lcd_cursor(0,1);
		lcd_msg("ENVIANDO DATOS..");
		//serial_println_str(tipoDesecho);	 
                serial_println_str(cantidadDesechos);
		_delay_ms(2000);
		lcd_clrscr();
		lcd_msg("**COMPLETADO**");
		_delay_ms(1000);
                lcd_clrscr();
		key2="";
		cantidadDesechos[0]="";
		memset(str,0,20);
    }
}
