// 定义二叉搜索树节点类
class TreeNode {
    constructor(key) {
        this.key = key;
        this.left = null;
        this.right = null;
    }
}

// 定义二叉搜索树类
class BinarySearchTree {
    constructor() {
        this.root = null;
    }

    // 插入节点
    insert(key) {
        const newNode = new TreeNode(key);
        if (this.root === null) {
            this.root = newNode;
        } else {
            this._insertNode(this.root, newNode);
        }
    }

    _insertNode(node, newNode) {
        if (newNode.key < node.key) {
            if (node.left === null) {
                node.left = newNode;
            } else {
                this._insertNode(node.left, newNode);
            }
        } else {
            if (node.right === null) {
                node.right = newNode;
            } else {
                this._insertNode(node.right, newNode);
            }
        }
    }

    // 在二叉搜索树中查找最接近给定值的节点
    findClosest(key) {
        return this._findClosestNode(this.root, key);
    }

    _findClosestNode(node, key, closest = null) {
        if (node === null) {
            return closest;
        }

        if (closest === null || Math.abs(node.key - key) < Math.abs(closest.key - key)) {
            closest = node;
        }

        if (key < node.key) {
            return this._findClosestNode(node.left, key, closest);
        } else if (key > node.key) {
            return this._findClosestNode(node.right, key, closest);
        } else {
            return node;
        }
    }
}

// 将对象转换成二叉搜索树
function objectToBST(obj) {
    const bst = new BinarySearchTree();
    for (let key in obj) {
        bst.insert(parseInt(key));
    }
    return bst;
}

// 示例使用
const myObj = {
    10: "value1",
    5: "value2",
    15: "value3",
    3: "value4",
    7: "value5"
};

const bst = objectToBST(myObj);
console.log(bst.findClosest(8)); // 输出: TreeNode { key: 7, left: TreeNode { key: 5, ... }, right: null }
