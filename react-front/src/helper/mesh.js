import { triangles } from './constants.js'

export const drawMesh = (predictions, ctx, width) => {
    // Draw every point in the mesh
    if (predictions.length > 0) {
        predictions.forEach(prediction => {
            const keypoints = prediction.scaledMesh;

            // Draw triangles
            for (let i = 0; i < triangles.length/3; i++) {
                const points = [
                    triangles[i*3],
                    triangles[i*3+1],
                    triangles[i*3+2],
                ].map((index) => keypoints[index]);
                drawPath(ctx, points, width);
            }

            // Draw points
            for (let i = 0; i < keypoints.length; i++) {
                const x = width-keypoints[i][0]; // Reflect over the x-axis
                const y = keypoints[i][1];

                ctx.beginPath();
                ctx.arc(x, y, 1, 0, 3*Math.PI);
                ctx.fillStyle = '#7289da';                
                ctx.globalAlpha = 0.25;
                ctx.fill();
            }
        })
    }

}

const drawPath = (ctx, points, width) => {
    // Initialize path
    const region = new Path2D();
    region.moveTo(width-points[0][0], points[0][1]);

    // Connect all points in points
    for (let i = 1; i < points.length; i++) {
        const point = points[i];
        region.lineTo(width-point[0], point[1]);
    }

    region.closePath();

    ctx.strokeStyle = 'black';
    // ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = 0.25;
    ctx.stroke(region);
}
