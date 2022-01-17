#include "avr/io.h"
#include "util/delay.h"
#include "lcd.h"
#include "uart.h"

int main(void)
{
	serial_begin();
    i2c_init();
    lcd_init();
	
	char tipoDesecho;
	int cantidadDesechos;
	char key;
	
	kbrd_init();
	
	lcd_msg("   BIENVENIDO");
	lcd_cursor(1,0);
    _delay_ms(1000);
	lcd_msg("   AL PROGRAMA   ");
	_delay_ms(1000);
	lcd_clrscr();
	
    while(1)
    {
		//PANTALLA DE PREGUNTA DE RESIDUO INDUSTRIAL
        lcd_cursor(0,0);	  	
        lcd_msg(" RESIDUO (I/NI)");
		lcd_cursor(1,0);
		lcd_msg("  I:ON    NI:=");
		do{
			key=kbrd_read();
			tipoDesecho=key;
		}while (!(key!='='^key!='.'));
		//PANTALLA DE SELCCION DE KILOS
		lcd_clrscr();
		//lcd_home();
        lcd_cursor(0,0);
		lcd_msg("CANTIDAD BASURA:");
		cantidadDesechos=1;
        char cdch = "";
		do{
			if(kbrd_read()=='+' && cantidadDesechos<9){cantidadDesechos++;}
			else if (kbrd_read()=='-' && cantidadDesechos>1){cantidadDesechos--;}
			lcd_cursor(1,0);
			cdch = cantidadDesechos + "0";
			lcd_msg(cdch);
			lcd_cursor(1,4);
			lcd_msg("KG");
			key=kbrd_read();

		}while(key!='=');
        
		//PANTALLA DE ENVIO DE DATOS
		lcd_clrscr();
		//lcd_home();
        lcd_cursor(0,1);
		lcd_msg("ENVIANDO DATOS..");
		_delay_ms(2000);
		lcd_clrscr();
		//lcd_home();
		lcd_msg("**COMPLETADO**");
		_delay_ms(1000);
        lcd_clrscr();
		{
		}

    }
}
