export function setupFetchStub(data) {
    return function fetchStub(_url) {
        return new Promise((resolve) => {
            resolve(data)
        })
    }
}

export function compareElementsTextToArray(elementsArray, valuesArray) {
    elementsArray.forEach((element, index) => {
        expect(element.textContent).toEqual(valuesArray[index]);
    })
}