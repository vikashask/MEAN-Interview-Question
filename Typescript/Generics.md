Without generics, we would either have to give the identity function a specific type:

function identity(arg: number): number {
    return arg;
}

function identity(arg: any): any {
    return arg;
}

Generic Types