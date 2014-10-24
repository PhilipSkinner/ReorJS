/*
 * Genetic equation generator example v1.0.0
 * Author(s): Philip Skinner
 * Last modified: 2014-09-28
 *
 * --
 * Simple mutation only genetic program that finds equations that equal a 
 * specified target number.
 *
 * Is a compatible reorjsd application.
 * --
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,     
 * but WITHOUT ANY WARRANTY; without even the implied warranty of      
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright (c) 2014, Crowdcalc B.V.                                                                                                                      
*/

function(id, data) {
  //target number
  var target = 42;
  //mutation rate
  var mutationRate = 0.05;

  //our decoded 4 bit commands
  var commands = {
    '0000' : 0,
    '0001' : 1,
    '0010' : 2,
    '0011' : 3,
    '0100' : 4,
    '0101' : 5,
    '0110' : 6,
    '0111' : 7,
    '1000' : 8,
    '1001' : 9,
    '1010' : '+',
    '1011' : '-',
    '1100' : '*',
    '1101' : '/',
    '1110' : 'unknown',
    '1111' : 'unknown',
  };

  //name: decode
  //arguments: dna
  //function: takes a valid dna string and decodes it based upon our command set.
  function decode(dna) {
    var parts = dna.match(/..../g);
    var instruction = '';
  
    if (parts) {  	  
      for (var i = 0; i < parts.length; i++) {
        instruction += commands[parts[i]];
      }
    }
  
    return instruction;  
  }

  //name: generateParts
  //arguments: num, length
  //function: generates <num> dna strings of <length>
  function generateParts(num, length) {
    var parts = [];
    for (var i = 0; i < num; i++) {
      var part = '';
      for (var j = 0; j < length; j++) {
        part += String(Math.round(Math.random()));
        part += String(Math.round(Math.random()));
        part += String(Math.round(Math.random()));
        part += String(Math.round(Math.random()));
      }
      parts.push(part);
    }
  
    return parts;
  }

  //name: determineFitness
  //arguments: value
  //function: determines the fitness of the passed <value>
  function determineFitness(value) {
    if (target - value == 0) {
      return 1;
    }    
  
    if (Math.abs(target - value) == 1) {
      return 0.9999999;
    }
  
    return 1/(target-value);
  }

  //generate our initial DNA strings
  var parts = generateParts(5, 4);

  var solution = false;
  var loops = 0;
  while (solution == false) {
    var best = '';
    var bestScore = 0;
    var second = '';
    var secondScore = 0; 
         
    for (var i = 0; i < parts.length; i++) {
      var fitness = 0;
      try {
        var value = eval(decode(parts[i]));
        fitness = determineFitness(value);      
      } catch(e) {
        fitness = 0;  
      }
    
      if (fitness == 1) {
        //we have a solution, return the data to reorjs
        solution = true;
        return { id : { code : parts[i], decoded : decode(parts[i]), cycles : loops } };
      }

      if (fitness >= bestScore) {
        if (bestScore >= secondScore) {
          secondScore = fitness;
          second = best + '';
        }
    
        bestScore = fitness;
        best = parts[i] + '';      
      } else if (fitness >= secondScore) {
        secondScore = fitness;
        second = parts[i] + '';
      }        
    }
  
    //mutate
    var mutated = [];  
    for (var i = 0; i < parts.length; i++) {
      var seq = parts[i].split('');
      var newS = '';
      for (var j = 0; j < seq.length; j++) {
        var chance = Math.random();
        if (chance < mutationRate) {
          if (seq[j] == '0') {
            newS += '1';
          } else {
            newS += '0';
          }
        } else {
          newS += seq[j] + '';
        }
      } 
    
      mutated.push(newS);       
    }  
  
    parts = mutated;
    loops++;
  }
}
