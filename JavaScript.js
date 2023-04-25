function func(){
  const xhttp = new XMLHttpRequest();
  // Define a callback function
  xhttp.onload = function () {
    k=this.responseText.split(',')
      
      
      
      br=document.createElement('br')
      form = document.getElementById("one");
      

    if(k!=""){
      Length=k.length/3 
      console.log(k)
    for (let i = 0; i < Length; i++) {
      
      input = document.createElement("input")
      node= document.createElement("label")
      text=document.createTextNode(k[i*3])
      br=document.createElement('br')
    // let op="option"
    // let id=op.concat(x)
    // console.log(id)
      input.setAttribute('type', 'radio')
      input.setAttribute('required',true)
      input.setAttribute('id', k[i*3])
      input.setAttribute('value', k[i*3])
      input.setAttribute('name', 'molecules')
      form.appendChild(input);
      node.setAttribute('for', k[i*3])
      node.appendChild(text)

      form.appendChild(node)
      form.appendChild(br)

      input = document.createElement("b")
      input.setAttribute('class', 'bold')
      textBond=" --bonds="+k[(i*3)+1]
      text=document.createTextNode(textBond)
      form = document.getElementById("one");
      input.appendChild(text)
      form.appendChild(input)
      form.appendChild(br)
      input = document.createElement("b")
      input.setAttribute('class', 'bold')
      textAtom="--Atom="+k[(i*3)+2]
      text=document.createTextNode(textAtom)
      form = document.getElementById("one");
      input.appendChild(text)
      form.appendChild(input)
      form.appendChild(br)
    }
    header=document.createElement("h3")
    Htext=document.createTextNode("Would you also like to rotate this molecule?")
    header.appendChild(Htext)
    form.appendChild(header)

    input = document.createElement("input")
    node= document.createElement("label")
    text=document.createTextNode("Rotation axis(x,y,z):")
    br=document.createElement('br')

    input.setAttribute('type', 'text')
    input.setAttribute('id', 'option1')
    input.setAttribute('name', 'rotationaxis')
    
    node.setAttribute('id', 'option1')
    node.appendChild(text)

    form.appendChild(node)
    form.appendChild(input);
    form.appendChild(br)
    


    input = document.createElement("input")
    node= document.createElement("label")
    text=document.createTextNode(" Degree of rotation:")

    input.setAttribute('type', 'text')
    input.setAttribute('id', 'option2')
    input.setAttribute('name', 'Degree')

    node.setAttribute('id', 'option2')
    node.appendChild(text)

    form.appendChild(node)
    form.appendChild(input);
    form.appendChild(br)

// <form action="senddata.html" multipart/form-data method="post">
//     <label id="element number">Rotation axis(x,y,z):</label><br>
//     <input type="text" id="elementnumber" name="elementnumber"><br>
//     <label id="element code">Degree of rotation:</label><br>
//     <input type="text" id="elementcode" name="elementcode"><br>

  inputF = document.createElement("input")
  inputF.setAttribute('type','submit')
  inputF.setAttribute('value','Submit')
  inputF.setAttribute('id','button')
  form.appendChild(inputF)
  }
      
}

// Send a request
xhttp.open("GET", "createbutton");
xhttp.send();
}

func();

function showTB(){
  const xhttp = new XMLHttpRequest();
  // Define a callback function
  xhttp.onload = function () {
    console.log(this.responseText)
    table=docuemnt.getElementById("table")
    input = document.createElement("tr")
    input2 = document.createElement("th")
    text=document.createTextNode("new")
    table.appendChild(input);
    input.appendChild(input2)
    input2.appendChild(text)
    
//     <tr>
//     <th>ELEMENT_NO</th>
//     <th>ELEMENT_CODE</th>
//     <th>ELEMENT_NAME</th>
//     <th>COLOUR1</th>
//     <th>COLOUR2</th>
//     <th>COLOUR3</th>
//     <th>RADIUS</th>
// </tr>
}
// Send a request
xhttp.open("POST", "showTB");
xhttp.send();
}


