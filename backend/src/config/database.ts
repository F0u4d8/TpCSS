import _default = require("@prisma/client");

// Singleton pattern for Prisma Client
const prismaClientSingleton = () => {
return new _default.PrismaClient({
log: ['error', 'warn'],
});
};

declare global {
var prisma: undefined | ReturnType<typeof prismaClientSingleton>;
}

const prisma = globalThis.prisma ?? prismaClientSingleton();

export default prisma;

if (process.env.NODE_ENV !== 'production') globalThis.prisma = prisma;