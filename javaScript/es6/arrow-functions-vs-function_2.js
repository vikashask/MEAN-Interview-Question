// 'this' here is exports

this.objectName = "The Exports Object";
console.log(this); // { objectName: 'The Exports Object' }

const testerObj = {
  // Regular Function
  func1: function () {
    console.log("func1", this); // func1 { func1: [Function: func1], func2: [Function: func2] }
  },

  // Arrow Function
  func2: () => {
    console.log("func2", this); // func2 { objectName: 'The Exports Object' }
  },
};

testerObj.func1();
testerObj.func2();
