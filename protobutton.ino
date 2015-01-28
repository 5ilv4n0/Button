/**
 * Free your ProtoButton 1.0
 */



byte dim[36]; // the led brightness values, ordered R1,B1,G1,R2,B2,G2,...
byte buffer[36];
byte table[8*8]; // the internal bit modulation matrix output table

// the setup routine runs once when you press reset:
void setup() {
  PORTD=0;

  // Serial.begin(9600);

  cli();
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for osc/blendMax period
  OCR1A = 255;
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // set prescaler osc/64
  TCCR1B |= (1 << CS11) | (1 << CS10);
  TIMSK1 = 1 << OCIE1A; // enable timer compare interrupt
  sei();

}

// interrupt routine to do the bit value modulation
byte currentRow=0;
byte currentBit=0;
byte rowStart=0;
ISR(TIMER1_COMPA_vect)
{
  OCR1A=255;

  // check for negative overflow, indicating we have passed bit 0.
  // then we select the next matrix row and begin with the highest value
  // bit again.
  if(currentBit==255) {
    currentRow++;
    if(currentRow>6) currentRow=0;

    byte output=B100<<currentRow;
    PORTB= output | B1; // | B1 to keep HDD in pullup on pin 0 up
    DDRB = output;

    currentBit=7; // highest value bit first
    rowStart=currentRow*8;
  }

  DDRD=table[rowStart+currentBit]; // set LED power according to modulation table

  OCR1A = 1<<(int)currentBit; // schedule next interrupt by bit value
  TCNT1 = 0;
  currentBit--;
}



void loop() {
	Serial.print('ready.\n');

	byte i=0;

	while(true) {
		
	  // receive command letter, speed and offset value on serial in
	  
	  while(Serial.available()>0){
		byte b=Serial.read();
	
		if(b == '\n') {
			for(byte c=0; c<36; c++){ 
				dim[c] = buffer[c];
			}
			buffer = [];
			
			
			// build bit value modulation table for current led power values
			for(byte row=0; row<6; row++)
			{
				// for this row, flash by bits of increasing significance
				for(byte i=0; i<8; i++){
					byte i_power_of_two=1<<i;
					byte d=0;
					for(byte col=0; col<6; col++) {
						byte v=dim[row*6+col];
						if(col!=0 && col!=3) v/=2; // red pixel too large resistor value fix
						if(v & i_power_of_two) d|=1<<col;
					}
					// write column outputs
					table[row*8+i]=d;
				}
			}
			delay(10);	
				
		}
		else {
			buffer[i] = b;
			i++;
		}
	  }
	}
}
